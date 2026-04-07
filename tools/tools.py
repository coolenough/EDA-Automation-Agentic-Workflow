import langchain_core.tools import tool
import pandas as pd
import numpy as np
import os
import io

@tool
def info(df : pd.DataFrame):
    ''' Gives the basic information about the given dataframe such as
    type of data , column info, size and shape of the dataframe as a pandas dataframe'''

    IO = io.StringIO()
    df.info(buf = IO)
    return IO.getvalue()
@tool
def describe(df : pd.DataFrame):
    '''
    Gives the statistical description of numerical dtypes as pandas dataframe
    '''
    return df.describe()

@tool
def walkthrough_directory():
    '''
    Gives the walkthrough of files in current directory
    '''
    return os.walk()

tools = [info,describe,walkthrough_directory]
