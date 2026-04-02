import langchain_core.tools import tool
import pandas as pd
import numpy as np

@tool
def info(df : pd.DataFrame):
    ''' Gives the basic information about the given dataframe such as
    type of data , column info, size and shape of the dataframe '''
    return df.info()
