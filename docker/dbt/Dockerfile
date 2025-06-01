FROM python:3.10-slim

# 1. Set working dir
WORKDIR /usr/app

# 2. Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Fix protobuf version and install DBT Spark with PyHive support
RUN pip install --upgrade pip && \
    pip install "protobuf<4.25.0" dbt-core==1.7.7 dbt-spark[PyHive]==1.7.1

# 4. Set DBT as default entrypoint
ENTRYPOINT ["dbt"]
