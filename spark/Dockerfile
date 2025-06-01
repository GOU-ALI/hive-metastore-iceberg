FROM apache/spark:3.5.3

# 1. Ajout des JARs nécessaires
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.7.2/iceberg-spark-runtime-3.5_2.12-1.7.2.jar /opt/spark/jars/
ADD https://jdbc.postgresql.org/download/postgresql-42.6.0.jar /opt/spark/jars/

# 2. Installation du pip + dépendances Python (optionnel pour PySpark)
USER root
RUN pip install --upgrade pip && pip install pandas pyspark

# 3. Ajout du script de démarrage du Thrift Server
COPY start-thriftserver.sh /opt/spark/start-thriftserver.sh
RUN chmod +x /opt/spark/start-thriftserver.sh

# 4. Lancer Spark Thrift Server automatiquement
ENTRYPOINT ["/opt/spark/start-thriftserver.sh"]
