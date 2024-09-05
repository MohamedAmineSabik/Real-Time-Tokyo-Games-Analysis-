import logging
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json,col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace created successfully!")

def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.created_users (
        id UUID PRIMARY KEY,
        Rank number ,
        Countries TEXT,
        GOLD number,
        SILVER number,
        BRONZE number,
        TOTAL number );
    """)

    print("Table created successfully!")

def insert_data(session, **kwargs):
    print("inserting data...")

    user_id = kwargs.get('id')
    Rank = kwargs.get('Rank')
    Countries = kwargs.get('Countries')
    GOLD = kwargs.get('GOLD')
    SILVER = kwargs.get('SILVER')
    BRONZE = kwargs.get('BRONZE')
    TOTAL = kwargs.get('TOTAL')

    try:
        session.execute("""
            INSERT INTO spark_streams.created_users(id, Rank, Countries, GOLD, SILVER, 
                BRONZE, TOTAL )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, Rank, Countries, GOLD, SILVER,
              BRONZE, TOTAL))
        logging.info(f"Data inserted for {Rank} {Countries}")

    except Exception as e:
        logging.error(f'could not insert data due to {e}')

def create_spark_connection():
    s_conn = None
    try:
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()
        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the Spark session due to exception: {e}")

    return s_conn

def connect_to_kafka(spark_conn):
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'olympic_games_results') \
            .option('startingOffsets', 'earliest') \
            .option("kafka.connection.timeout.ms", "10000") \
            .load()
        logging.info("Kafka DataFrame created successfully")
        return spark_df
    except Exception as e:
        logging.error(f"Kafka DataFrame could not be created because: {e}")
        return None

def create_cassandra_connection():
    try:
        # connecting to the cassandra cluster
        cluster = Cluster(['localhost'])

        cas_session = cluster.connect()

        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None


def create_selection_df_from_kafka(spark_df):
    if spark_df is None:
        raise ValueError("The input DataFrame 'spark_df' is None. Please provide a valid DataFrame.")
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("Rank", IntegerType(), False),
        StructField("Countries", StringType(), False),
        StructField("GOLD", StringType(), False),
        StructField("SILVER", IntegerType(), False),  # Numeric column example
        StructField("BRONZE", StringType(), False),
        StructField("TOTAL", StringType(), False)
    ])
    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    print(sel)
    return sel

if __name__ == "__main__":
    spark_conn = create_spark_connection()
    if spark_conn is not None:
        try:
            spark_df = connect_to_kafka(spark_conn)
            if spark_df is None:
                logging.error("Failed to create Kafka DataFrame.")
            else:
                logging.info("Successfully created Kafka DataFrame.")
        except Exception as e:
            logging.error(f"Error in streaming process: {e}")



