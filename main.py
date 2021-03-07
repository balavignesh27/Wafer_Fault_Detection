from flask import Flask, request, render_template
from flask import Response
import json
from training_Validation_Insertion import Train_Validation
from training_Model import Train_Model
from prediction_Validation_Insertion import Pred_Validation
from predictFromModel import Prediction


app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/train',methods=['GET','POST'])
def trainRouteClient():
    try:
        #path = 'Training_Batch_Files'
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
        train_valObjs = Train_Validation(path) # Object initialization
        train_valObjs.train_validation() # Calling the training_validation function

        trainModelObj = Train_Model() # Object initialization
        trainModelObj.trainingModel() # Calling the trainingModel function

    except ValueError:
        return Response('Error Occurred! %s'%ValueError)
    except KeyError:
        return Response('Error Occurred! %s'%KeyError)
    except Exception as e:
        return Response('Error Occurred! %s'%e)
    return Response('Training Successful!!')

@app.route('/predict', methods=['GET','POST'])
def predictRouteClient():
    try:
        # path = 'Prediction_Batch_files'
        if request.json is not None:
            path = request.json['filepath']
            pred_val = Pred_Validation(path)
            pred_val.prediction_validation()

            prediction = Prediction(path)
            path,json_predictions = prediction.predictionFromModel()

            return Response('Prediction File created at !!! '+str(path)+' and few of the predictions are\n'+str(json.loads(json_predictions)))

        elif request.form is not None:
            path = request.form['filepath']

            pred_val = Pred_Validation(path)
            pred_val.prediction_validation()

            prediction = Prediction(path)
            path,json_predictions = prediction.predictionFromModel()

            return Response('Prediction File created at !!!'+str(path)+' and few of the predictions are\n'+str(json.loads(json_predictions)))


        else:
            print('Nothing Matched')

    except ValueError:
        return Response('Error Occured! %s'%ValueError)
    except KeyError:
        return Response('Error Occurred! %s'%KeyError)
    except Exception as e:
        return Response('Error Occurred! %s'%e)



if __name__ == '__main__':
    app.run()


