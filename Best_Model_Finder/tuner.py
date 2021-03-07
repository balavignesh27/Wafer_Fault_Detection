from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score

class Model_Finder:

    """ This class shall be used to find the model with best accuracy and AUC score """

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rfc = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')

    def get_best_params_for_random_forest(self,train_x,train_y):

        """ Method: get_best_params_for_random_forest
            Description: get the parameters for Random Forest Algorithm which gives the best accuracy.
            Outcome: The model with best parameters by Hyper Parameter Tuning.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the get_best_params_for_Random_Forest method')
        try:
            #Initializing with different combination of parameter
            self.param_grid = {'n_estimators':[10,50,100,130],
                               'criterion':['gini','entropy'],
                               'max_depth':[2,3,4,5],
                               'max_features':['auto','log2']}
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.rfc, param_grid=self. param_grid, cv=5, verbose=3)
            # Finding the best parameters
            self.grid.fit(train_x,train_y)
            # Extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # Creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # Training the new model
            self.clf.fit(train_x,train_y)

            self.logger_object.log(self.file_object,'Random Forest best params: '+str(self.grid.best_params_))

            return self.clf

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in get_best_params_for_Random_Forest method')
            raise e

    def get_best_params_for_xgboost(self,train_x,train_y):

        """ Method: get_best_params_for_xgboost
            Description: get the parameters for XGBoost Algorithm which gives the best accuracy.
            Outcome: The model with best parameters by Hyper Parameter Tuning.
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_XGBoost method')
        try:
            # Initializing with different combination of parameters
            self.param_grid_xgboost = {'learning_rate':[0.5,0.1,0.01,0.001],
                                       'max_depth':[3,5,10,20],
                                       'n_estimators':[10,50,100,200]}
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(XGBClassifier(objective='binary:logistic'), self.param_grid_xgboost,
                                     cv=5, verbose=3)
            # Finding the best parameters
            self.grid.fit(train_x,train_y)
            # Extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # Creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth,
                                     n_estimators=self.n_estimators)
            # Training the new model
            self.xgb.fit(train_x,train_y)

            self.logger_object.log(self.file_object, 'XGBoost best params: ' + str(self.grid.best_params_))

            return self.xgb

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_params_for_XGBoost method')
            raise e

    def get_best_model(self,train_x,train_y,test_x,test_y):

        """ Method: get_best_model
            Description: Find out the Model which has the best AUC score.
            Outcome: The best model name and the model objecct
            On Failure: Raise Exception """

        self.logger_object.log(self.file_object,'Entered the get_best_model method')
        try:
            # Predictions using the XGBoost Model
            self.xgboost = self.get_best_params_for_xgboost(train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)
            if len(test_y.unique())==1:
                # If there is only one label in y, then ro_auc_score return error, in that case use accuracy_error
                self.xgboost_score = accuracy_score(test_y,self.prediction_xgboost)
                self.logger_object.log(self.file_object,'Accuracy for XGBoost: '+str(self.xgboost_score))
            else:
                self.xgboost_score = roc_auc_score(test_y,self.prediction_xgboost) # AUC for XGBoost
                self.logger_object.log(self.file_object,'AUC for XGBoost: '+str(self.xgboost_score))

            # Predictions using the Random Forest
            self.random_forest =self.get_best_params_for_random_forest(train_x,train_y)
            self.prediction_random_forest = self.random_forest.predict(test_x)
            if len(test_y.unique()==1):
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)
                self.logger_object.log(self.file_object,'Accuracy for RF: '+str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y,self.prediction_random_forest) # AUC for Random Forest
                self.logger_object.log(self.file_object,'AUC for RF: '+str(self.random_forest_score))

            # Comparing the two models
            if(self.random_forest_score < self.xgboost_score):
                return 'XGBoost', self.xgboost
            else:
                return 'RandomForest', self.random_forest

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in get_best_model Model')
            raise e






