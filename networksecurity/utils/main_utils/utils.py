from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml
import dill
import pickle
import numpy as np
import os,sys 


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str,content:dict,replace:bool =False):

    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        dir = os.path.dirname(file_path)
        os.makedirs(dir,exist_ok=True) 
        with open(file_path,"w") as file:
            yaml.dump(content,file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_numpy_array(filepath:str,array:np.array)->None:
    '''
    filepath:string location of file to save
    array: np.array data to save
    '''
    try:
        dir = os.path.dirname(filepath)
        os.makedirs(dir,exist_ok=True)
        with open(filepath,'wb') as file_object:
            np.save(file_object,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 

def save_object(filepath:str,obj:object)->None:
    try:
        logging.info("Entered the save object method")
        dir = os.path.dirname(filepath)
        os.makedirs(dir,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save object method")
    except Exception as e:
        raise NetworkSecurityException(e,sys)