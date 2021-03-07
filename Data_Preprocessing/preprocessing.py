import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:

    """ This class shall be used to clean and transform the data before training. """

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self,data,columns):

        """ Method Name: remove_columns
            Description: This method removes the given columns 'Wafer' from a pandas dataframe.
            Output: A pandas DataFrame after removing the specified columns 'Wafer'.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the remove_column method of the Preprocessor class')
        self.data = data
        self.columns = columns

        try:
            self.useful_data = self.data.drop(self.columns,axis=1)
            self.logger_object.log(self.file_object,'Column removal Successful!!')
            return self.useful_data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured %s'%e)
            raise e

    def seperate_label_feature(self,data,label_column_name):

        """ Method Name: remove_columns
            Description: This method separates the features and a Label Columns.
            Output: Return two separate Dataframes, one containing features and the other containing Labels.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(label_column_name,axis=1) # drop the target column
            self.Y = data[label_column_name] # Filter the label columns
            self.logger_object.log(self.file_object,'Label Separation Successful!!')

            return self.X, self.Y

        except Exception as e:
            self.logger_object.log(self.file_object,'Label Seperation Unsuccessful.')
            raise e

    def is_null_present(self,data):

        """ Method Name: is_null_present
            Description: This method checks whether there are null values present in the data or not
            Output: Returns a Boolean Value.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the is_null_present method')
        self.null_present = False

        try:
            self.null_counts = data.isna().sum()  # Check for the count of null vales per column
            for i in self.null_counts:
                if i>0:
                    self.null_present = True
                    break

            if(self.null_present):  # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv('Data_Preprocessing/null_values.csv')  # storing the null column information to file
                self.logger_object.log(self.file_object,'Finding missing values is Successful!!')

                return self.null_present

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in is_null_present method.%s'%e)
            raise e

    def impute_missing_values(self,data):

        """ Method Name: impute_missing_values
            Description: This method replaces all the missing values in the DataFrame using KNNImputer.
            Output: A DataFrame which has all the missing values imputed.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the impute_missing_values method')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data) # impute the missing values

            # Convert the nd-array returned in the step above to a Dataframe
            self.new_data = pd.DataFrame(self.new_array,columns=self.data.columns)
            self.logger_object.log(self.file_object,'Imputing missing values Successful!!')

            return self.new_data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in impute_missing_values method.%s'%e)
            raise e

    def get_columns_with_zero_std_deviation(self,data):

        """ Method Name: get_columns_with_zero_std_deviation
            Description: This method finds out the columns which have a standard deviation.
            Output: List of the columns with standard deviation of zero.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the get_columns_with_zero_std_deviation method')
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in self.columns:
                if self.data_n[x]['std']==0:  # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero

            self.logger_object.log(self.file_object,'Column search for Standard Deviation of Zero Successful!!')

            return self.col_to_drop

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in get_columns_with_zero_std_deviation method')
            raise e

