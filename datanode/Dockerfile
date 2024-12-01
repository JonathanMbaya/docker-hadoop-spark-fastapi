FROM openjdk:8-jdk-slim

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y openssh-server rsync bash curl procps && \
    rm -rf /var/lib/apt/lists/*


# Créer le répertoire pour le service SSH
RUN mkdir -p /run/sshd
RUN mkdir -p /opt/hadoop/logs && chmod 777 /opt/hadoop/logs


# Définir les variables d'environnement Hadoop
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Installer Hadoop
RUN mkdir -p /opt && \
    curl -L https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | \
    tar -xz -C /opt/hadoop --strip-components=1


# Installer HBase
ENV HBASE_VERSION=2.6.1
ENV HBASE_HOME=/opt/hbase
ENV PATH=$PATH:$HBASE_HOME/bin

RUN curl -L https://downloads.apache.org/hbase/$HBASE_VERSION/hbase-$HBASE_VERSION-bin.tar.gz | \
    tar -xz -C /opt && \
    mv /opt/hbase-$HBASE_VERSION $HBASE_HOME

# Configurer SSH pour l'accès sans mot de passe
RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys

# Copier les fichiers de configuration
COPY core-site.xml $HADOOP_CONF_DIR/
COPY hdfs-site.xml $HADOOP_CONF_DIR/
COPY yarn-site.xml $HADOOP_CONF_DIR/
COPY mapred-site.xml $HADOOP_CONF_DIR/
COPY hbase-site.xml $HBASE_HOME/conf/

# Copier le script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports nécessaires
EXPOSE 50075

# Définir le point d'entrée
CMD ["/entrypoint.sh"]
