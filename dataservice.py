from pyspark.sql import SparkSession
from settings_handler import settings
import pandas as pd
import sqlalchemy


def get_data():
    con = get_dbconn()
    df = pd.read_sql_table("datos_inversiones", con)
    df.drop(["index"], axis=1)
    return df


def get_session():
    return SparkSession.builder.master(settings.spark).getOrCreate()


def get_dbconn():
    return sqlalchemy.create_engine(settings.dbconn)


def get_investment(municipality):
    spark = get_session()
    data = pd.read_sql_table("investments", dbengine)
    return municipality


def get_x_y(x, y):
    return x, y


def get_model_predictions(model):
    return model
