#!/bin/bash

# Définir les variables Spark
export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Démarrer le service SSH
echo "Démarrage du service SSH..."
/usr/sbin/sshd

# Démarrer le Spark Master
echo "Démarrage de Spark Master..."
$SPARK_HOME/sbin/start-master.sh

# Démarrer le Spark Worker (optionnel)
echo "Démarrage de Spark Worker..."
$SPARK_HOME/sbin/start-worker.sh spark://localhost:7077

# Vérifier les processus Java
echo "Processus Spark démarrés :"
jps

# Garder le conteneur actif
tail -f /dev/null
