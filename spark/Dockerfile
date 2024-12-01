# Utiliser une image officielle de Hadoop 3.3 ou Ubuntu comme base
FROM ubuntu:20.04

# Installer Java requis pour Spark
RUN apt-get update && apt-get install -y openjdk-11-jdk curl && \
    apt-get clean
    
# Installer OpenSSH et autres dépendances nécessaires
USER root
RUN apt-get update && apt-get install -y openssh-server curl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/sshd

# Télécharger Spark 3.4.4 avec Hadoop 3.3
ENV SPARK_VERSION=3.4.4
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
RUN curl -O https://dlcdn.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    tar -xvf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    mv spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION $SPARK_HOME && \
    rm spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz

# Configurer PATH
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# Copier le fichier entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports pour Spark
EXPOSE 7077 8080

CMD ["/entrypoint.sh"]
