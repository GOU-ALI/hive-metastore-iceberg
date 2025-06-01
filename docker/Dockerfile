# ┌─────────────────────────────────────────────────────────────────────┐
# │ Dockerfile for Hive Metastore + Iceberg backed by PostgreSQL       │
# └─────────────────────────────────────────────────────────────────────┘
FROM openjdk:8-jre-slim

ARG HADOOP_VER=3.3.4
ARG HIVE_VER=3.1.3

# 1) Install prerequisites including net-tools for netstat
RUN apt-get update \
 && apt-get install -y netcat procps postgresql-client net-tools curl \
 && rm -rf /var/lib/apt/lists/*

# 2) Unpack Hadoop into /opt/hadoop
COPY docker/hadoop-${HADOOP_VER}.tar.gz /tmp/
RUN mkdir -p /opt/hadoop \
 && tar -xzf /tmp/hadoop-${HADOOP_VER}.tar.gz -C /opt/hadoop --strip-components=1 \
 && rm /tmp/hadoop-${HADOOP_VER}.tar.gz

ENV HADOOP_HOME=/opt/hadoop
ENV PATH="$HADOOP_HOME/bin:$PATH"

# 3) Unpack Hive standalone-metastore into /opt/hive-metastore
COPY docker/hive-standalone-metastore-${HIVE_VER}-bin.tar.gz /tmp/
RUN mkdir -p /opt/hive-metastore \
 && tar -xzf /tmp/hive-standalone-metastore-${HIVE_VER}-bin.tar.gz -C /opt/hive-metastore --strip-components=1 \
 && rm /tmp/hive-standalone-metastore-${HIVE_VER}-bin.tar.gz

ENV HIVE_HOME=/opt/hive-metastore
ENV PATH="$HIVE_HOME/bin:$PATH"

# 4) Copy in JDBC, AWS-SDK & Iceberg jars
COPY docker/drivers/postgresql-42.6.0.jar           $HIVE_HOME/lib/postgresql.jar
COPY docker/drivers/aws-java-sdk-bundle-1.12.599.jar $HIVE_HOME/lib/aws-java-sdk-bundle.jar
COPY docker/drivers/iceberg-hive-runtime-1.7.2.jar   $HIVE_HOME/lib/iceberg-hive-runtime.jar
RUN cp $HADOOP_HOME/share/hadoop/tools/lib/hadoop-aws-${HADOOP_VER}.jar \
        $HIVE_HOME/lib/
    
# 5) Copy in configs and entrypoint
COPY config/core-site.xml        $HIVE_HOME/conf/core-site.xml
COPY config/hive-site.xml        $HIVE_HOME/conf/hive-site.xml
COPY config/iceberg.properties   $HIVE_HOME/conf/iceberg.properties
COPY scripts/entrypoint.sh       /scripts/entrypoint.sh

RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT ["/scripts/entrypoint.sh"]