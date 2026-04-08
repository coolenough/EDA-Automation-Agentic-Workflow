from langchain_core.tools import tool
import pandas as pd
import numpy as np
import os
import io
import subprocess
import sys

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



tools = [info,describe,walkthrough_directory,install_packages]
