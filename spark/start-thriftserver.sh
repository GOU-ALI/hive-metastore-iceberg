#!/bin/bash

/opt/spark/sbin/start-thriftserver.sh \
  --master local[*] \
  --conf spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog \
  --conf spark.sql.catalog.spark_catalog.type=hive \
  --conf spark.sql.catalog.spark_catalog.uri=thrift://hive-metastore:9083 \
  --conf spark.sql.catalog.spark_catalog.warehouse=s3a://iceberg-warehouse/warehouse \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=password \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --conf spark.hadoop.fs.s3a.connection.ssl.enabled=false \
  --hiveconf hive.server2.thrift.port=10000


echo "[INFO] ThriftServer launched. Now tailing logs to keep container alive..."

# 👇 Bloquer le conteneur en affichant les logs
tail -f /opt/spark/logs/spark--org.apache.spark.sql.hive.thriftserver.HiveThriftServer2-*.out