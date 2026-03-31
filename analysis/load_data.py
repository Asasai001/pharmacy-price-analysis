import pandas as pd
from db_connection import get_engine

def load_query(query):
    engine = get_engine()
    df = pd.read_sql(query, engine)
    return df
