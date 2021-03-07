import json
import os
from os import listdir
import shutil
import re
import pandas as pd
from application_logging import logger

class Raw_Data_validation:
    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = logger.App_Logger()

    def valuesFromSchema(self):

        """ Method Name: valuesFromSchema
            Description: This method extracts all the relevant information from the pre-defined 'Schema' file.
            Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noOfColumns
            On Failure: Raise ValueError, KeyError, Exception   """

        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberOfColumns = dic['NumberofColumns']

            file = open('Training_Logs/valuesFromSchemaValidationLog.txt','a+')
            message = 'LengthOfDateStampInFile:: %s'%LengthOfDateStampInFile+'\t'+'LengthOfTimeStampInFile:: %s'%LengthOfTimeStampInFile+'\t'+'NumberOfColumns:: %s'%NumberOfColumns+'\n'

            self.logger.log(file,message)
            file.close()

        except ValueError:
            file = open('Training_Logs/valuesFromSchemaValidation.txt','a+')
            message = 'ValueError: Value not found inside schema_training.json'
            self.logger.log(file,message)
            file.close()
            raise ValueError

        except KeyError:
            file = open('Training_Logs/valuesFromSchemaValidation.txt','a+')
            message = 'KeyError: Key value error incorrect key passed'
            self.logger.log(file,message)
            file.close()
            raise KeyError

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns

    def manualRegExCreation(self):

        """ Method Name: manualRegExCreation
            Description: This contains a manually defined regex based on the 'Filename' given in 'Schema' file.
            Output: RegEx pattern
            On Failure: None  """

        regex = "wafer+\_+\d\d\d\d\d\d\d\d+\_+\d\d\d\d\d\d+\.csv$"
        return regex

    def deleteExistingBadDataTrainingFolder(self):

        """ Method Name: deleteExistingBadDataTrainingFolder
            Description: This method deletes the directory made to store the bad data.
            Output: None
            On Failure: OSError  """

        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path+'Bad_Raw/'):
                shutil.rmtree(path+'Bad_Raw/')
                file = open('Training_Logs/GeneralLog.txt','a+')
                self.logger.log(file,'BadRaw directory deleted before starting validation')
                file.close()
        except OSError as s:
            file = open('Training_Logs/GeneralLog.text','a+')
            self.logger.log(file,'Error while deleting directory:%s'%s)
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):

        """ Method Name: deleteExistingBadDataTrainingFolder
            Description: This method deletes the directory made to store the good data.
            Output: None
            On Failure: OSError  """

        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path+'Good_Raw/'):
                shutil.rmtree(path+'Good_Raw/')
                file = open('Training_logs/GeneralLog.txt','a+')
                self.logger.log(file,'GoodRaw directory deleted before starting validation')
                file.close()
        except OSError as s:
            file = open('Training_logs/GeneralLog.txt', 'a+')
            self.logger.log(file, 'Error while deleting directory:%s'%s)
            file.close()
            raise OSError

    def createDirectoryForGoodBadFinalRawData(self):

        """ Method Name: createDirectoryForGoodBadRawData
            Description: This method creates directories to store the Good Data, Bad Data and Final single concatenated
                data from Good data
            Output: None
            On Failure: OSError  """

        try:
            path = os.path.join('Training_Raw_files_validated/','Good_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join('Training_Raw_files_validated/','Bad_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join('Training_Raw_files_validated/', 'Final_Validated_data/')
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as s:
            file = open('Training_logs/GeneralLog.txt','a+')
            self.logger.log(file,'Error while creating Directory %s'%s)
            file.close()
            raise OSError

    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):

        """ Method Name: validationFileNameRaw
            Description: This function validates the name of the training csv files as per given name in the schema!
                RegEx pattern is used to do the validation. If name format do not match the file is moved
                to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception  """

        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.deleteExistingFinalValidatedInputFile()
        self.createDirectoryForGoodBadFinalRawData()


        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:
            file = open('Training_Logs/nameValidationLog.txt','a+')
            for filename in onlyfiles:
                if (re.match(regex,filename)):
                    splitAtDot = re.split('.csv',filename)
                    splitAtDot = re.split('_',splitAtDot[0])
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy('Training_Batch_Files/'+filename,'Training_Raw_files_validated/Good_Raw')
                            self.logger.log(file,'Valid File Name!! File moved to Good Raw Folder::%s'%filename)
                        else:
                            shutil.copy('Training_Batch_Files/'+filename,'Training_Raw_files_validated/Bad_Raw')
                            self.logger.log(file, 'Valid File Name!! File moved to Bad Raw Folder::%s'%filename)
                    else:
                        shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Bad_Raw')
                        self.logger.log(file, 'Valid File Name!! File moved to Bad Raw Folder::%s' % filename)
                else:
                    shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Bad_Raw')
                    self.logger.log(file, 'Valid File Name!! File moved to Bad Raw Folder::%s' % filename)
            file.close()

        except Exception as e:
            file = open('Training_Logs/nameValidationLog.txt', 'a+')
            self.logger.log(file,'Error occured while validating FileName %s'%e)
            file.close()
            raise e

    def validateColumnLength(self,NumberOfColumns):

        """ Method Name: validationFileNameRaw
            Description: This function validates the number of columns in the csv files.
                It is should be same as given i nthe schema file.
                If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                If the column number matches, file is kept in Good Raw Data for processing
                The csv file is missing the first column name, this function changes the missing name to 'Wafer'.
            Output: None
            On Failure: Exception  """

        try:
            file = open('Training_Logs/columnValidationLog.txt','a+')
            self.logger.log(file,'Column Length Validation Started!!')
            for filename in listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv(r'Training_Raw_files_validated/Good_Raw/'+filename)
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move('Training_Raw_files_validated/Good_Raw/'+filename,'Training_Raw_files_validated/Bad_Raw/')
                    self.logger.log(file,'Invalid Column Length for the file!! File moved to Bad Raw Folder:%s'%filename)
            self.logger.log(file,'Column Length Validation Completed!!')
            file.close()

        except OSError:
            file = open('Training_Logs/columnValidationLog.txt','a+')
            self.logger.log(file,'Error Occured while moving the file:%s'%OSError)
            file.close()
            raise OSError

        except Exception as e:
            file = open('Training_Logs/columnValidationLog.txt', 'a+')
            self.logger.log(file, 'Error Occured:%s' %e)
            file.close()
            raise e

    def validateMissingValuesInWholeColumn(self):

        """ Method Name: validationFileNameRaw
            Description: This function validates if any column in the csv file has all values missing.
                If all the values are missing, the file is not suitable for processing.
                Such files are moved to bad raw data.
            Output: None
            On Failure: Exception  """

        try:
            file = open('Training_Logs/missingValueInColumn.txt','a+')
            self.logger.log(file,'Missing values Validation Started!!')

            for f in listdir('Training_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv('Training_Raw_files_validated/Good_Raw/'+f)
                count=0
                columns = df.columns
                for column in columns:
                    if (len(df[column]) - df[column].count()) == len(df[column]):
                        count+=1
                        shutil.move('Training_Raw_files_validated/Good_Raw/'+f, 'Training_Raw_files_validated/Bad_Raw')
                        self.logger.log(file, 'Invalid Column Length for the file!! File moved to Bad Raw Folder:%s'%f)
                        break
                    if count==0:
                        df.rename(columns={'Unnamed: 0':'Wafer'}, inplace=True)
                        df.to_csv('Training_Raw_files_validated/Good_Raw/'+f, index=None, header=True)


        except OSError:
            file = open('Training_Logs/missingValueInColumn.txt','a+')
            self.logger.log(file,'Error Occured while moving the file:%s'%OSError)
            file.close()
            raise OSError

        except Exception as e:
            file = open('Training_Logs/missingValueInColumn.txt', 'a+')
            self.logger.log(file, 'Error Occured:%s' %e)
            file.close()
            raise e

    def deleteExistingFinalValidatedInputFile(self):

        """ Method Name: deleteExistingFinalValidatedInputFile
            Description: This method deletes the directory made to store the Final Validated Input data for training.
            Output: None
            On Failure: OSError  """

        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path+'Final_Validated_data/'):
                shutil.rmtree(path+'Final_Validated_data/')
                file = open('Training_logs/GeneralLog.txt', 'a+')
                self.logger.log(file, 'Final Input file directory deleted before starting validation')
                file.close()

        except OSError as s:
            file = open('Training_logs/GeneralLog.txt', 'a+')
            self.logger.log(file, 'Error while deleting directory:%s' % s)
            file.close()
            raise OSError


    def finalValidatedInputFile(self):

        """ Method Name: finalValidatedInputFile
            Description: This method creates a directory of final Input File for training.
            Output: None
            On Failure: OSError  """

        try:
            file = open('Training_Logs/finalValidatedInputFile.txt', 'a+')
            self.logger.log(file, 'Final Validated Input File creation started!!')
            path = 'Training_Raw_files_validated/Good_Raw'
            files = [f for f in listdir(path)]
            count = 0
            dataset = pd.read_csv(path + '/' + files[0])
            for file in files:
                if count > 0:
                    merge_dataset = pd.read_csv(path + '/' + file)
                    dataset = pd.concat([dataset, merge_dataset], axis=0)
                else:
                    count += 1

            dataset.to_csv('Training_Raw_files_validated/Final_Validated_data/InputFile.csv', index=None, header=True)
            file = open('Training_Logs/finalValidatedInputFile.txt', 'a+')
            self.logger.log(file, 'Final Validated Input File creation Successful!!')
            file.close()

        except OSError as s:
            file = open('Training_logs/GeneralLog.txt', 'a+')
            self.logger.log(file, 'Error while deleting directory:%s' % s)
            file.close()
            raise OSError












