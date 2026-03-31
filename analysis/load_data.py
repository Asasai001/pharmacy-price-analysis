import pandas as pd
from analysis.db_connection import get_engine

engine = get_engine()

def load_query(query):
    df = pd.read_sql(query, engine)
    return df
