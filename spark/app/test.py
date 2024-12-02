from pyspark.sql import SparkSession

def main():
    # Créez une session Spark
    spark = SparkSession.builder \
        .appName('Test Spark Submit') \
        .getOrCreate()

    # Chargez le fichier CSV
    inputfile = './testdata.csv'
    outputpath = '/output/'

    df = spark.read.option('header', 'true').csv(inputfile)

    # Transformation : comptez les occurrences par valeur
    result = df.groupBy('value').count()

    # Affichez les résultats dans la console
    result.show()

    # Sauvegardez les résultats dans un fichier (format CSV)
    result.write.mode('overwrite').csv(outputpath)

    # Arrêtez la session Spark
    spark.stop()

if __name__ == '__main__':
    main()