import pickle
import os
import shutil

class File_Operation:

    """ This class shall be used to save the model after training
        and load the saved model for prediction """

    def __init__(self,file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'Models/'

    def save_model(self,model,filename):

        """ Method: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the save_model method.')
        try:
            path = os.path.join(self.model_directory,filename)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)

            f = open(path+'/'+filename+'.pkl','wb')
            pickle.dump(model,f)
            self.logger_object.log(self.file_object,'Model File '+filename+' saved.')
            f.close()
            return 'Success'

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in save_model method')

    def load_model(self,filename):

        """ Method: load_model
            Description: Load the model file to memory
            Output: The Model file loaded in memory
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the load_model method')
        try:
            f = open(self.model_directory+filename+'/'+filename+'.pkl','rb')
            self.logger_object.log(self.file_object,'Model File '+filename+' loaded.')

            return pickle.load(f)

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in load_model method. %s'%e)
            raise e

    def find_correct_model_file(self,cluster_number):

        """ Method: find_correct_model_file
            Description: Select the correct model based on cluster number
            Output: The Model file
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the find_correct_model_file method')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_files = list(os.listdir(self.folder_name))

            for self.file in self.list_of_files:
                try:
                    if str(self.cluster_number) in self.file:
                        model = self.load_model(self.file)
                        return model
                except:
                    continue

            self.logger_object.log(self.file_object,'Exited the find_correct_model_file method!!')

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in find_correct_model_file method')
            raise e


