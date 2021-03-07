import pandas as pd
from File_Operations import file_methods
from Data_Preprocessing import preprocessing
from Data_Ingestion import data_loader_prediction
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation

class Prediction:

    def __init__(self,path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        if path is not None:
            self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):

        try:
            self.pred_data_val.deletePredictionFile() # deletes the existing prediction file from last run!
            self.log_writer.log(self.file_object,'Start of Prediction')
            data_getter=data_loader_prediction.Data_Getter_Pred(self.file_object,self.log_writer)
            data=data_getter.get_data()

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            is_null_present = preprocessor.is_null_present(data)
            if (is_null_present):
                data = preprocessor.impute_missing_values(data)

            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(data)
            data = preprocessor.remove_columns(data, cols_to_drop)

            # Load the cluster model
            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            # Predict the clusters
            clusters = kmeans.predict(data.drop('Wafer',axis=1)) # Drop the Wafer Column
            data['Clusters'] = clusters
            clusters = data['Clusters'].unique()

            for i in clusters:
                cluster_data = data[data['Clusters']==i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(['Wafer','Clusters'],axis=1)

                # Predict the clustered data
                model_predict = file_loader.find_correct_model_file(i)
                result = list(model_predict.predict(cluster_data))

                # Create a csv file to store the result dataframe
                result = pd.DataFrame(list(zip(wafer_names,result)),columns=['Wafer','Prediction'])
                path = "Prediction_Output_File/Predictions.csv"
                result.to_csv('Prediction_Output_File/Predictions.csv',index=None,header=True,mode='a+') # Appends the result

            self.log_writer.log(self.file_object, 'End of Prediction')

        except Exception as e:
            self.log_writer.log(self.file_object, 'Error occurred while running the prediction!! Error:: %s' % e)
            raise e

        return path, result[result['Prediction']==1].to_json(orient="records")

