from pyspark.sql import functions as F
from pyspark.sql import types as T

from utils.pspark import setup_spark
from utils.config import parse_configs, get_secret
from utils.proto import getdataresponse
from udf.ml import scorer, lowpassfilterscorer
from udf.proto import *
from udf.utils import gettime, getpreferences, matchpreferences
from udf.proto import content_schema



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
    df.show(20, False)
    
    # Writing the topic after HP filter
    highpass_transformed = (
        df
        .withColumn("Content", F.struct("contentId"))
        .groupBy("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId")
        .agg(
            F.collect_list("content").alias("content")
        )
        .withColumn("value", (serialize_for_analytics(F.struct("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId", "content"), F.lit("USERZAPPWIDGET"))))
        .withColumn("key", F.col("userid"))
        .select("key","value")
    )
    # highpass_transformed.write.parquet("gs://glance-ds-gcs-non-prod-sg-001/pipeline_name=itemtouserfanout/version=1.1.0/region=in/widgetid=BREAKINGNEWS", mode="overwrite")
    
    
    
    # Adding the model score 
    scorer_transformed = (
        df
        .withColumn("score", scorer("startTime"))
        .withColumn("Content", F.struct("contentId", "score"))
        .groupBy("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId")
        .agg(
            F.collect_list("content").alias("content")
        )
        .withColumn("processEndTime", gettime("userId"))
        .withColumn("key", F.col("userid"))
        .withColumn("value", (serialize_for_scorer(F.struct("jobId", "userId", "zappWidgetId", "processStartTime", "processEndTime", "experimentVariantId", "content"), F.lit("USERZAPPWIDGET"))))
        .select("key","value")
    )
    # scorer_transformed.write.parquet("gs://glance-ds-gcs-non-prod-sg-001/pipeline_name=itemtouserfanout_scorer/version=1.1.0/region=in/widgetid=BREAKINGNEWS",  mode="overwrite")
    
    if env == "DEV":
        highpass_transformed.show(200, False)
        scorer_transformed.show(200, False)
    else:
    
        (
            highpass_transformed
            .write
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_CREDENTIALS["bootstrap.servers"])    
            .option("kafka.sasl.jaas.config","org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(KAFKA_CREDENTIALS['sasl.username'], KAFKA_CREDENTIALS['sasl.password']))
            .option("kafka.ssl.endpoint.identification.algorithm", "https")
            .option("kafka.group.id", kafka_config['ui.group.id'])
            .option("kafka.security.protocol", kafka_config["security.protocol"])
            .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
            .option("topic", kafka_config['analytics.output.topic'])
            .option("checkpointLocation", gcp_config["ui.checkpoint.analytics.location"])
            # .options(**kafka_configs) 
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
            .option("kafka.group.id", kafka_config['ui.group.id'])
            .option("kafka.security.protocol", kafka_config["security.protocol"])
            .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
            .option("topic", kafka_config['output.topic'])
            .option("checkpointLocation", gcp_config["ui.checkpoint.location"])
            # .options(**kafka_configs) 
            .save()
        )
        
        df.unpersist()



# %%
if __name__ == '__main__':
    
    config_file = 'config.ini'
    conf = parse_configs(config_file)
    kafka_config = dict(conf.items('kafka-config'))
    gcp_config = dict(conf.items('gcp-config'))
    env_config = dict(conf.items('env-config'))
    bq_config = dict(conf.items('bq-config'))
    KAFKA_CREDENTIALS = get_secret(gcp_config["project.number"], kafka_config["secret.id"], parse_json=True)
                   
    spark = setup_spark(bq_config['dataset.id'])


    inputdf = (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_CREDENTIALS["bootstrap.servers"])    
        .option("kafka.sasl.jaas.config","org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(KAFKA_CREDENTIALS['sasl.username'], KAFKA_CREDENTIALS['sasl.password']))
        .option("kafka.ssl.endpoint.identification.algorithm", "https")
        .option("kafka.group.id", kafka_config['ui.group.id'])
        .option("kafka.security.protocol", kafka_config["security.protocol"])
        .option("kafka.sasl.mechanism", kafka_config["sasl.mechanisms"])
        .option("subscribe", kafka_config['input.user.topic'])
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "false")
        .load() # Load from Kafka topic
    )


    # Transforming the input - content items
    inputtransformed = (
        inputdf
        .select(F.col("value"))
        .withColumn("processStartTime", gettime(F.lit(1)))
        .withColumn("deserialized", deserialize_user_preferences("value"))
        .select("deserialized.userId", "deserialized.jobId", "deserialized.zappWidgetId",
               "deserialized.partnerId", "deserialized.region", "processStartTime",
                "deserialized.preferences"
               )
        # .withColumn("region", F.lit("IN"))
    )
    

    # Reading the data items-metadata-url
    dataurl = 'http://uat-space-content-cms.sg2.internal.glance-np.glance.com/api/v1/spaces/contents?zappWidgetId={}'.format(kafka_config["zapp.widget.id"])
    dataarr = getdataresponse(dataurl)
    itemlist = spark.read.schema(content_schema).json(spark.sparkContext.parallelize(dataarr))

    # process itemlist
    itemlisttransformed = (
        itemlist
        .withColumnRenamed("preferences", "item_preferences")
        .drop("jobId")
    )
    itemlisttransformed.show(10, False)
        
        
    # Finding the relevant content for the user and High Pass Filters
    highpass_transformed = (
        itemlisttransformed
        .join(F.broadcast(inputtransformed), on=[ "zappWidgetId", "partnerId", "region"], how="inner")
        .withColumn("processEndTime", gettime("contentId")) 
        .withColumn("experimentVariantId", F.lit("model_v1"))
        .withColumn("match", matchpreferences("preferences", "item_preferences"))
        .filter("match==1")
    )


    # Writing into two separate queues
    (
        highpass_transformed
        .writeStream
        .foreachBatch(lambda df, epochId: write_to_output_topics(df, epochId, env_config["env"]))
        .start()
        .awaitTermination()
    )
