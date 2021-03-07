from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict
from application_logging import logger

class Pred_Validation:

    def __init__(self,path):
        self.raw_data = Prediction_Data_validation(path)
        self.dataTransform = dataTransformPredict()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):

        try:

            self.log_writer.log(self.file_object,'Start of Validation on files for prediction!!')
            #extracting values from prediction schema
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.raw_data.valuesFromSchema()
            #getting the regex defined to validate filename
            regex = self.raw_data.manualRegexCreation()
            #validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)
            #validating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)
            #validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object,"Raw Data Validation Complete!!")

            self.log_writer.log(self.file_object,("Starting Data Transforamtion!!"))
            #replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.file_object,"DataTransformation Completed!!!")

            self.log_writer.log(self.file_object, 'Final validated dataset creation started!!')
            self.raw_data.finalValidatedInputFile()
            self.log_writer.log(self.file_object, 'Final validated dataset creation Successful!!')

        except Exception as e:
            raise e

