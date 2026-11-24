from networksecurity.entity.config_entity import DataValidationConfig 
from networksecurity.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys 

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:    
        
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_date(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required Number of columns:{number_of_columns}")
            logging.info(f"DataFrame has {len(dataframe.columns)} columns")
            if number_of_columns == len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_data_drift(self,base_df,current_df,threshold =0.5)->bool:
        try:
            report={}
            status =True
            for col in base_df.columns:
                c1 =base_df[col]
                c2 =current_df[col]
                is_same_dist = ks_2samp(c1,c2)
                
                if is_same_dist.pvalue<threshold:
                    is_found =True
                    status =False
                else:
                    is_found =False
                report.update({
                            col:{"pvalue": float(is_same_dist.pvalue),
                            "Drift_Status":is_found}
                                    })
            drift_report_filepath = self.data_validation_config.data_drift_report_file_path
            dir = os.path.dirname(drift_report_filepath)
            os.makedirs(dir,exist_ok=True)
            write_yaml_file(file_path=drift_report_filepath,content=report)
            return status    

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path =  self.data_ingestion_artifact.train_file_path
            test_file_path =  self.data_ingestion_artifact.test_file_path
            
            ##read the data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            #validate the data
            status = self.validate_date(dataframe=train_df)
            if not status:
                error_message = f"Train Dataframe does not have all the columns.\n"
            status = self.validate_date(dataframe=test_df)
            if not status:
                error_message = f"Test Dataframe does not have all the columns.\n"

            #detect data drift
            status = self.detect_data_drift(base_df=train_df,current_df=test_df)            
           
            if status==True:#possible data drift
                dir=os.path.dirname(self.data_validation_config.invalid_train_data_filepath)
                os.makedirs(dir,exist_ok=True)
                train_df.to_csv(self.data_validation_config.invalid_train_data_filepath,index=False,header=True)
                test_df.to_csv(self.data_validation_config.invalid_test_data_filepath,index=False,header=True)
            else:
                dir=os.path.dirname(self.data_validation_config.valid_train_data_filepath)
                os.makedirs(dir,exist_ok=True)
                train_df.to_csv(self.data_validation_config.valid_train_data_filepath,index=False,header=True)
                test_df.to_csv(self.data_validation_config.valid_test_data_filepath,index=False,header=True)

            
            data_validation_artifact = DataValidationArtifact(
                validation_status=True,
                valid_train_file_path = self.data_validation_config.valid_train_data_filepath,
                valid_test_file_path = self.data_validation_config.valid_test_data_filepath,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.data_drift_report_file_path
            )

            return data_validation_artifact 
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    



