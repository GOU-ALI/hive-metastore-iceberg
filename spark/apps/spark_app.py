from pyspark.sql import SparkSession
import pandas as pd
# Configuration Spark avec Iceberg
spark = SparkSession.builder \
    .appName("IcebergApp") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .config("spark.sql.catalog.spark_catalog.uri", "thrift://hive-metastore:9083") \
    .config("spark.sql.catalog.spark_catalog.warehouse", "s3a://iceberg-warehouse/warehouse") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .getOrCreate()




#spark.sql("SHOW TABLES IN default").show()

#spark.sql("""
#  CREATE TABLE default.gouali_iceberg (
#    name STRING,
#    age INT
#  )
#  USING iceberg
#""")
#
#data = [("abdou1", 30), ("gouali1", 25)]
#columns = ["name", "age"]
##spark.sql("SHOW TABLES IN default").show()
##
#df = spark.createDataFrame(data, columns)
#df.write.format("iceberg").mode("append").save("default.gouali_iceberg")
### Création d'une table Iceberg
#df.writeTo("default.ma_table_iceberg").using("iceberg").createOrReplace()
##
### Lecture des données
#result = spark.sql("SELECT * FROM default.gouali_iceberg")
#result.show()

# Fonctionnalités Iceberg
res = spark.sql("SELECT * FROM default.gouali_iceberg.history")
res.show()
res1 = spark.sql("SELECT * FROM default.gouali_iceberg.snapshots")
res1.show()
print("==============LIRE MANIFEST =================")
spark.read.format("iceberg").load("default.gouali_iceberg.manifests").show(truncate=False)
    
    