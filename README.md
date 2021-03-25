# Wafer_Fault_Detection

To know about the project, read the Problem Statement.docx and the Program architecture.ppt

To run the project, follow the below steps.
1. Download all the files.
2. Install PyCharm.
3. Open the "main.py" file.
4. In the terminal type -> pip install -r requirements.txt
5. After installing all the necessary libraries.
6. Run the main.py file.
7. Open the localhost in the web browser.
8. You can see the Web API to predict the wafer quality.
9. Place the Folder path of which csv files need to be predicted in the text box. Here it is "Prediction_Raw_Files_Validated".
10. Click the Custom File Predict and you can see the output. You will also get the output csv file in "Prediction_Output_File" folder.
11. In case you want to train the model again.
12. Install Postman.
13. Pass the URL:localhost:5000/train and along with that send the file's folder path which you want to train as json format. Here it is 'folderPath':'Training_Batch_Files'.
14. After getting output "Training Successful", do the prediction as mentioned above.

Thank you.
