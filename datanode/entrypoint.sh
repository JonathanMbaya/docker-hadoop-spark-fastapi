#!/bin/bash

# Définir les variables d'environnement Hadoop
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$PATH
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root


# Démarrer le service SSH
echo "Démarrage du service SSH..."
/usr/sbin/sshd

# Vérifier si le DataNode est déjà formaté
if [ ! -d "/hadoopdata/hdfs/datanode/current" ]; then
    echo "Formatage du DataNode..."
    mkdir -p /hadoopdata/hdfs/datanode
    chown -R root:root /hadoopdata/hdfs/datanode
    $HADOOP_HOME/bin/hdfs datanode -format -force
fi

# Démarrer le DataNode
echo "Démarrage du DataNode..."
$HADOOP_HOME/bin/hdfs datanode

# Démarrer le NodeManager pour YARN
echo "Démarrage du NodeManager..."
$HADOOP_HOME/bin/yarn nodemanager

# Vérifier les processus Java (debug)
echo "Processus Hadoop démarrés :"
jps

# Garder le conteneur actif
tail -f /dev/null
