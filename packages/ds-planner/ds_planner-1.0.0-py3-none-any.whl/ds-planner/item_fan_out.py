from pyspark.sql import functions as F
from pyspark.sql import types as T

from utils.pspark import setup_spark
from utils.config import parse_configs, get_secret
from utils.proto import getdataresponse
from udf.ml import scorer, lowpassfilterscorer
from udf.proto import *
from udf.utils import gettime, getpreferences, matchpreferences


def write_to_output_topics(df, epoch_id, env):
    """
    For each writer that writes the df into two kafka topics
    
    Args:
        df : Dataframe that is output from the stream query
        epoch_id : identifier
    Returns:
        Writes to console / topic
    """
    # Persisting the Dataframe
    df.cache()
    df.select("jobId", "contentId", "zappWidgetId").distinct().show(2000, False)
    
    # Writing the topic after HP filter
    highpass_transformed = (
        df
        .withColumn("content", F.array(F.struct("contentId")))
        .withColumn("processEndTime", gettime("contentId"))
        .withColumn("value", (serialize_for_analytics(F.struct("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId", "content"), F.lit("CONTENT"))))
        .withColumn("key", F.col("userid"))
        .select("key","value")
    )
    
    # Adding the model score 
    scorer_transformed = (
        df
        
        .withColumn("score", scorer("startTime")) # scorer for each userid * contentid
        .withColumn("key", F.col("userid"))
        .withColumn("content", F.array(F.struct("contentId", "score")))
        .withColumn("processEndTime", gettime("userId"))
        .withColumn("value", (serialize_for_scorer(F.struct("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId", "content"), F.lit("CONTENT"))))
        .select("key","value")
    )
    
    print("Environment: ", env)
    if env == "DEV":
        highpass_transformed.show(2000, False)
        scorer_transformed.show(2000, False)
    else:
        (
            highpass_transformed
            .write
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_CREDENTIALS["bootstrap.servers"])    
            .option("kafka.sasl.jaas.config","org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(KAFKA_CREDENTIALS['sasl.username'], KAFKA_CREDENTIALS['sasl.password']))
            .option("kafka.ssl.endpoint.identification.algorithm", "https")
            .option("kafka.group.id", kafka_config['iu.group.id'])
            .option("kafka.security.protocol", kafka_config["security.protocol"])
            .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
            .option("topic", kafka_config['analytics.output.topic'])
            .option("checkpointLocation", gcp_config["iu.checkpoint.analytics.location"])
            .partitionBy("key")
            .save()

        )

        (
            scorer_transformed
            .write
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_CREDENTIALS["bootstrap.servers"])    
            .option("kafka.sasl.jaas.config","org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(KAFKA_CREDENTIALS['sasl.username'], KAFKA_CREDENTIALS['sasl.password']))
            .option("kafka.ssl.endpoint.identification.algorithm", "https")
            .option("kafka.group.id", kafka_config['iu.group.id'])
            .option("kafka.security.protocol", kafka_config["security.protocol"])
            .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
            .option("topic", kafka_config['output.topic'])
            .option("checkpointLocation", gcp_config["iu.checkpoint.location"])
            .save()
        )
        
        df.unpersist()


# %%
if __name__ == '__main__':
    
    config_file = 'config.ini'
    conf = parse_configs(config_file)
    kafka_config = dict(conf.items('kafka-config'))
    print(kafka_config)
    gcp_config = dict(conf.items('gcp-config'))
    env_config = dict(conf.items('env-config'))
    bq_config = dict(conf.items('bq-config'))
    KAFKA_CREDENTIALS = get_secret(gcp_config["project.number"], kafka_config["secret.id"], parse_json=True)
    
    # from py4j.java_gateway import java_import
    spark = setup_spark(bq_config['dataset.id'])
    # java_import(spark._sc._jvm, "org.apache.spark.sql.api.python.*")
                   
    # protoProcessUdf = ProtoProcessUdf("CONTENT")
    


    inputdf = (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_CREDENTIALS["bootstrap.servers"])    
        .option("kafka.sasl.jaas.config","org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(KAFKA_CREDENTIALS['sasl.username'], KAFKA_CREDENTIALS['sasl.password']))
        .option("kafka.ssl.endpoint.identification.algorithm", "https")
        .option("kafka.group.id", kafka_config['iu.group.id']) 
        .option("kafka.security.protocol", kafka_config["security.protocol"])
        .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
        .option("subscribe", kafka_config['input.topic'])
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "false")
        .load() # Load from Kafka topic
    )


    # Transforming the input - content items
    input_transformed = (
        inputdf
        .select("value")
        .withColumn("processStartTime", gettime(F.lit("key")))
        .withColumn("value", deserialize_content_cms("value"))
        .select("value.jobId", "value.contentId", "value.startTime", "value.region", "value.partnerId", 
                "value.zappWidgetId", "value.preferences", "processStartTime")
    )
    

    # Reading the data from user-data bigquery
    sql = """
      SELECT userprefstore.user_id as userId, userstore.region, userstore.partner_id AS partnerId, userprefstore.group_id, TO_JSON_STRING(userprefstore.group_data) AS group_data_string
      FROM user_data.user_pref_grouping_changelog as userprefstore
      INNER JOIN user_data.sp_v2_user_changelog as userstore
      ON userprefstore.user_id = userstore.user_id
      """
    
    # .format(kafka_config["zapp.widget.id"])

    userlist = (
        spark.read.format("bigquery").load(sql)
        .withColumn("user_preferences", getpreferences("group_data_string"))
        .select("userId", "region", "partnerId", "user_preferences")

    )
    userlist.show(1, False)

        
    # Fan-Out to Users and High Pass Filters
    highpass_transformed = (
        userlist
        .join(F.broadcast(input_transformed), on=["partnerId",'region'], how='inner') # removing the zappWidgetId filter
        .withColumn("match", matchpreferences("user_preferences", "preferences"))
        .filter("match==1")
        .withColumn("experimentVariantId", F.lit("model_v1"))
    )

    # Calling foreach to write into two topics
    (
        highpass_transformed
        .writeStream
        .foreachBatch(lambda df, epochId: write_to_output_topics(df, epochId, env_config["env"]))
        .start()
        .awaitTermination()
    )

