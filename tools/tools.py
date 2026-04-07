import langchain_core.tools import tool
import pandas as pd
import numpy as np
import os

@tool
def info(df : pd.DataFrame):
    ''' Gives the basic information about the given dataframe such as
    type of data , column info, size and shape of the dataframe as a pandas dataframe'''
    return df.info()
@tool
def describe(df : pd.DataFrame):
    '''
    Gives the description of numerical types of data as pandas dataframe
    '''
    return df.describe()

@tool
def walkthrough_directory():
    '''
    Gives the walkthrough to current directory
    '''
    return os.walk()

tools = [info,describe,walkthrough_directory]
