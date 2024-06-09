# Dockerfile for MongoDB Config, Shard, and Router Nodes

FROM ubuntu:20.04
LABEL authors="jiny"

# Install dependencies and MongoDB
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget gnupg && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y mongodb-org && \
    rm -rf /var/lib/apt/lists/*

# Create MongoDB data directories
RUN mkdir -p /data/configdb /data/db

# Expose the default MongoDB ports
EXPOSE 27017 27018 27019

# Default command to run MongoDB
CMD ["mongod"]
