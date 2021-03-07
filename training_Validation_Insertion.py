from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from Data_Transform_Training.DataTransformation import Data_Transform
from application_logging import logger

class Train_Validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = Data_Transform()
        self.file_object = open('Training_Logs/Training_Main_Log.txt','a+')
        self.log_writer = logger.App_Logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object,'Start of Validation on files!!')
            # Extracting values from training schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noOfColumns = self.raw_data.valuesFromSchema()

            # Getting the RegEx defined to validate filename
            regex = self.raw_data.manualRegExCreation()

            # Validating filename of training files
            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile, LengthOfTimeStampInFile)

            # Validating column length in the file
            self.raw_data.validateColumnLength(noOfColumns)

            # Validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object,'Raw Data Validation Complete!!')


            self.log_writer.log(self.file_object,'Starting Data Transformation!!')
            #Replacing blanks in the csv file with 'Null' values
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.file_object,'Data Transformation Completed!!')

            self.log_writer.log(self.file_object,'Final validated dataset creation started!!')
            self.raw_data.finalValidatedInputFile()
            self.log_writer.log(self.file_object, 'Final validated dataset creation Successful!!')

            self.file_object.close()


        except Exception as e:

            raise e
