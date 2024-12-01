# Utiliser une image de base avec OpenJDK
FROM openjdk:8-jdk-slim

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    openssh-server \
    rsync \
    bash \
    curl \
    nano && \
    rm -rf /var/lib/apt/lists/*

# Définir les variables d'environnement pour Hadoop
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Télécharger et installer Hadoop
RUN mkdir -p /opt/hadoop && \
    curl -L https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | \
    tar -xz -C /opt/hadoop --strip-components=1

# Supprimer les références à sudo dans les scripts Hadoop
RUN if [ -f $HADOOP_HOME/libexec/hadoop-functions.sh ]; then \
        sed -i 's/sudo -n -u \$HDFS_NAMENODE_USER //g' $HADOOP_HOME/libexec/hadoop-functions.sh && \
        sed -i 's/sudo -n -u \$HDFS_DATANODE_USER //g' $HADOOP_HOME/libexec/hadoop-functions.sh && \
        sed -i 's/sudo -n -u \$HDFS_SECONDARYNAMENODE_USER //g' $HADOOP_HOME/libexec/hadoop-functions.sh; \
    else \
        echo "Fichier hadoop-functions.sh non trouvé, aucune modification effectuée"; \
    fi && \
    if [ -f $HADOOP_HOME/sbin/start-yarn.sh ]; then \
        sed -i 's/sudo -n -u \$YARN_RESOURCEMANAGER_USER //g' $HADOOP_HOME/sbin/start-yarn.sh && \
        sed -i 's/sudo -n -u \$YARN_NODEMANAGER_USER //g' $HADOOP_HOME/sbin/start-yarn.sh; \
    else \
        echo "Fichier start-yarn.sh non trouvé, aucune modification effectuée"; \
    fi

# Définir les variables d'environnement pour Hive
ENV HIVE_VERSION=4.0.1
ENV HIVE_HOME=/opt/hive
ENV PATH=$PATH:$HIVE_HOME/bin

# Télécharger et installer Hive
RUN mkdir -p /opt/hive && \
    curl -L https://downloads.apache.org/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz | \
    tar -xz -C /opt/hive --strip-components=1

# Supprimer les références à sudo dans les scripts Hive (si applicable)
RUN if [ -f $HIVE_HOME/bin/hive-config.sh ]; then \
        sed -i 's/sudo -n //g' $HIVE_HOME/bin/hive-config.sh; \
    else \
        echo "Fichier hive-config.sh non trouvé, aucune modification effectuée"; \
    fi

# Définir les variables d'environnement pour HBase
ENV HBASE_VERSION=2.6.1
ENV HBASE_HOME=/opt/hbase
ENV PATH=$PATH:$HBASE_HOME/bin

# Télécharger et installer HBase
RUN mkdir -p /opt/hbase && \
    curl -L https://downloads.apache.org/hbase/$HBASE_VERSION/hbase-$HBASE_VERSION-bin.tar.gz | \
    tar -xz -C /opt/hbase --strip-components=1

# Supprimer les références à sudo dans les scripts HBase (si applicable)
RUN if [ -f $HBASE_HOME/bin/hbase-config.sh ]; then \
        sed -i 's/sudo -n //g' $HBASE_HOME/bin/hbase-config.sh; \
    else \
        echo "Fichier hbase-config.sh non trouvé, aucune modification effectuée"; \
    fi

# Configurer SSH pour un accès sans mot de passe
RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys

# Copier les fichiers de configuration
COPY core-site.xml $HADOOP_CONF_DIR/
COPY hdfs-site.xml $HADOOP_CONF_DIR/
COPY yarn-site.xml $HADOOP_CONF_DIR/
COPY mapred-site.xml $HADOOP_CONF_DIR/
COPY hive-site.xml $HIVE_HOME/conf/
COPY hbase-site.xml $HBASE_HOME/conf/

# Copier le script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports nécessaires
EXPOSE 9870 8088 8080 10000 16010

# Définir le point d'entrée
CMD ["/entrypoint.sh"]
