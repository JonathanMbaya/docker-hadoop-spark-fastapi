#!/bin/bash

# Définir les utilisateurs Hadoop pour autoriser l'exécution en tant que root
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

# Démarrer le service SSH
echo "Démarrage du service SSH..."
/usr/sbin/sshd

# Vérifier si le NameNode est déjà formaté
if [ ! -d "/hadoopdata/hdfs/namenode/current" ]; then
    echo "Formatage du NameNode..."
    $HADOOP_HOME/bin/hdfs namenode -format -force
fi

echo "Démarrage du NameNode..."
$HADOOP_HOME/bin/hdfs --daemon start namenode

# Démarrer le SecondaryNameNode
echo "Démarrage du SecondaryNameNode..."
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

# Démarrer YARN (ResourceManager)
echo "Démarrage du ResourceManager..."
$HADOOP_HOME/bin/yarn --daemon start resourcemanager


# Vérifier les processus Java (debug)
echo "Processus Hadoop démarrés :"
jps

# Garder le conteneur actif
tail -f /dev/null
