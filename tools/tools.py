from langchain_core.tools import tool
import pandas as pd
import numpy as np
import os
import io
import subprocess
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import base64

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

@tool 
def install_packages(packages : list):
    '''
    installs required packages and returns list of installed packages as well as any packages that failed to install
    and the exception raised that failure
    '''

    installed_packages = []
    failed_packages = []

    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m","pip","install",package],
                                  timeout = 60)
            installed_packages.append(package)
        except subprocess.TimeoutExpired:
            failed_packages.append({"package": package, 
                                    "error": "Installation timed out after 60s"})
        except Exception as e:
            failed_packages.append({'package' : package,
                                    "error" : str(e)})
             
    return installed_packages,failed_packages

@tool 
def find_columns(df : pd.DataFrame):
    '''
    return columns in a Data Frame
    '''
    return list(df.columns)

@tool 
def box_plots(df : pd.DataFrame , columns : list):
    '''
    returns the box plots of the given columns 
    '''

    images = []
    for col in columns:
        plt.figure()
        sns.boxplot(df[col])
        buffer = io.BytesIO()
        plt.savefig(buffer,format = "png")
        imagebytes = buffer.getvalue()
        images.append(base64.b64encode(imagebytes).decode("utf-8"))
        plt.close()
        buffer.close()

    return images

@tool
def kde_plots(df : pd.DataFrame , columns : list):
    '''
    return the kde plots of the given columns 
    '''

    images = []
    for col in columns:
        plt.figure()
        sns.kdeplot(df[col] , fill = True , color="purple")
        buffer = io.BytesIO()
        plt.savefig(buffer,format = "png")
        imagebytes = buffer.getvalue()
        images.append(base64.b64encode(imagebytes).decode("utf-8"))
        plt.close()
        buffer.close()

    return images

@tool
def find_unique_values(df : pd.DataFrame , target : str):
    '''
    returns the unique classes in target
    '''
    return np.unique(df[target])

@tool 
def type_of_categotical_data(df : pd.DataFrame , columns : list):
    '''
    returns the column and its and the type of categorical data
    '''

    col_types = []

    for col in columns:
        num = len(np.unique(df[col]))
        if num > 2:
            col_types.append({"column" : col , "type" : "Multi Cardinal"})
        else:
            col_types.append({"column" : col , "type" : "Binary" })

    return col_types

@tool 
def piecharts(df : pd.DataFrame , columns : list):
    '''
    Generates pie charts for categorical columns.
    '''
    images = []
    for col in columns:
        # You need the value_counts() to make a pie chart!
        data = df[col].value_counts()
        
        plt.figure(figsize=(6, 6))
        plt.pie(data, labels=data.index, autopct='%1.1f%%')
        plt.title(f"Distribution of {col}")
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        
        images.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))
        buffer.close()

    return images


tools = [info,describe,walkthrough_directory,install_packages,box_plots,kde_plots,find_unique_values,type_of_categotical_data,piecharts]
