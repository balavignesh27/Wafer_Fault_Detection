import pandas as pd

class Data_Getter:

    """ This class shall be used for obtaining the data from the source for training./"""

    def __init__(self,file_object,logger_object):
        self.training_file = 'Training_Raw_files_validated/Final_Validated_data/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):

        """ Method Name: get_data
            Description: This method reads the data from source.
            Output: A pandas DataFrame.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the get_data method of the Data_Getter class')
        try:
            self.data = pd.read_csv(self.training_file)   # reading the data file
            self.data.rename(columns={'Good/Bad':'Output'},inplace=True)
            self.logger_object.log(self.file_object,'Data Load Successful. Exited the get_data method of the \
                                                    Data_Getter class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in get_data method of the Data_Getter class.\
                                                    Exception message:%s'%e)
            raise e