from os import listdir
import pandas as pd
from application_logging.logger import App_Logger

class Data_Transform:
    def __init__(self):
        self.goodDataPath = 'Training_Raw_files_validated/Good_Raw'
        self.logger = App_Logger()

    def replaceMissingWithNull(self):
        file = open('Training_Logs/dataTransformLog.txt','a+')
        try:
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file_name in onlyfiles:
                df = pd.read_csv(self.goodDataPath+'/'+file_name)
                df.fillna('NULL', inplace=True)
                df['Wafer'] = df['Wafer'].str[6:]
                df.to_csv(self.goodDataPath+'/'+file_name, index=None, header=True)
                self.logger.log(file, '%s:File Transformed successfully!!'%file_name)

        except Exception as e:
            self.logger.log(file,'Data Transformation failed because :%s'%e)
            file.close()
        file.close()