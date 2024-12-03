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

# Démarrer les services Hadoop
echo "Démarrage du NameNode..."
$HADOOP_HOME/bin/hdfs --daemon start namenode

echo "Démarrage du SecondaryNameNode..."
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

echo "Démarrage du ResourceManager..."
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

# Attendre que le NameNode soit actif avant de continuer
echo "Attente que le NameNode soit prêt..."
until $HADOOP_HOME/bin/hdfs dfs -ls / >/dev/null 2>&1; do
    echo "Le NameNode n'est pas prêt, nouvelle tentative dans 5 secondes..."
    sleep 5
done

# Configuration HDFS : création des répertoires et configuration des permissions
echo "Configuration des répertoires HDFS..."
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /gsod
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /gsod
echo "Répertoire /gsod créé avec succès et permissions définies."

# Vérifier les processus Hadoop
echo "Processus Hadoop démarrés :"
jps

# Garder le conteneur actif
tail -f /dev/null
