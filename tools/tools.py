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
from tools import cpptools
import pybind11



@tool
def info(filename : str):
    ''' Gives the basic information about the given dataframe such as
    type of data , column info, size and shape of the dataframe as a pandas dataframe'''

    df = pd.read_csv(filename)

    IO = io.StringIO()
    df.info(buf = IO)
    return IO.getvalue()
@tool
def describe(filename : str):
    '''
    Gives the statistical description of numerical dtypes as pandas dataframe
    '''

    df = pd.read_csv(filename)

    return df.describe().to_dict()

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
def find_columns(filename : str):
    '''
    return columns in a Data Frame
    '''

    df = pd.read_csv(filename)

    return list(df.columns)

@tool 
def box_plots(filename : str, columns : list):
    '''
    returns the box plots of the given columns 
    '''

    df = pd.read_csv(filename)
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
def kde_plots(filename : str , columns : list):
    '''
    return the kde plots of the given columns 
    '''

    df = pd.read_csv(filename)

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
def find_unique_values(filename : str , target : str):
    '''
    returns the unique classes in target
    '''
    
    df = pd.read_csv(filename)
    return np.unique(df[target])

@tool 
def type_of_categotical_data(filename : str , columns : list):
    '''
    returns the column and its and the type of categorical data
    '''

    df = pd.read_csv(filename)
    col_types = []

    for col in columns:
        num = len(np.unique(df[col]))
        if num > 2:
            col_types.append({"column" : col , "type" : "Multi Cardinal"})
        else:
            col_types.append({"column" : col , "type" : "Binary" })

    return col_types

@tool 
def piecharts(filename : str , columns : list):
    '''
    Generates pie charts for categorical columns.
    '''

    df = pd.read_csv(filename)
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

@tool
def findnullvalues(filename : str , columns : list):

    '''
    Returns whether the particular columns in the file contains some null values
    '''

    df = pd.read_csv(filename)

    results = []

    for col in columns:
        if df[col].isna().any():
            results.append({"column" : col , "containsnullvalues" : True})
        else:
            results.append({"column" : col , "containsnullvalues" : False})

    return results

@tool
def findnoofnullvalues(filename : str , columns : list):
    '''
    Returns no of null values in a particular column
    '''

    df = pd.read_csv(filename)

    results = []

    for col in columns:
        results.append({"column" : col , "noofnullvalues" : np.sum(df[col].isna().astype(int))}) 

    return results

@tool
def getFileName():
    '''
    Gets the filename and the relative path to directory where the file to examine exists
    '''

    filename = input("Enter file name : ")

    rel_path = input("Enter relative path : ")

    return {"filename" : filename , "relative_path" : rel_path}

@tool
def plot_correlation_heatmap(filename : str , columns : list):
    '''
    Plots the correlation heatmap for the given columns
    '''

    df = pd.read_csv(filename)

    plt.figure(figsize=(10, 8))
    sns.heatmap(df[columns].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    
    image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return image


agent_tools = [info,describe,walkthrough_directory,install_packages,box_plots,kde_plots,find_unique_values,type_of_categotical_data,piecharts,findnullvalues,findnoofnullvalues,getFileName,plot_correlation_heatmap]
