from sklearn.model_selection import train_test_split
from Data_Ingestion import data_loader
from Data_Preprocessing import preprocessing
from Data_Preprocessing import clustering
from Best_Model_Finder import tuner
from File_Operations import file_methods
from application_logging.logger import App_Logger

class Train_Model:

    def __init__(self):
        self.file_object = open('Training_Logs/ModelTrainingLog.txt', 'a+')
        self.log_writer = App_Logger()

    def trainingModel(self):

        # Logging the start of training
        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # objecct for Preprocessing
            preprocess = preprocessing.Preprocessor(self.file_object, self.log_writer)

            # Remove the Wafer column
            data_remove_columns = preprocess.remove_columns(data, 'Wafer')

            # Create separate features and labels
            X, Y = preprocess.seperate_label_feature(data_remove_columns, 'Output')

            # Check if missing values are present in the dataset, if yes call KNNImputer method
            is_null_present = preprocess.is_null_present(X)
            if is_null_present:
                X = preprocess.impute_missing_values(X)

            # Check which columns do not contribute to predictions
            # If the Standard Deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # Prepare the list of such column to drop
            cols_to_drop = preprocess.get_columns_with_zero_std_deviation(X)

            # Drop the columns obtained above
            X = preprocess.remove_columns(X, cols_to_drop)

            #  """  CLUSTERING  """

            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)  # Object initialization.
            number_of_clusters = kmeans.elbow_plot(X)  # Using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X = kmeans.create_clusters(X, number_of_clusters)

            # Create a new cluster column in the dataset consisting of the corresponding clusters
            X['Labels'] = Y

            # Getting the unique clusters from our dataset
            list_of_clusters = X['Cluster'].unique()

            # """  Parsing all the clusters and looking for the best ML algorithm to fit on individual cluster  """

            for i in list_of_clusters:
                cluster_data = X[X['Cluster'] == i]  # Filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # Splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=0.1,
                                                                    random_state=100)
                model_finder = tuner.Model_Finder(self.file_object, self.log_writer)  # Object initialization
                # Getting the best model for each of the clusters
                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

                # Saving the best model to the directory
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name + str(i))

            # Logging the Successful Training
            self.log_writer.log(self.file_object,'Successful End of Training')
            self.file_object.close()

        except Exception as e:
            # Logging the unsuccessful training
            self.log_writer.log(self.file_object,'Unsuccessful End of Training')
            self.file_object.close()