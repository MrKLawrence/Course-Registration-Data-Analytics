#model3
#!/usr/bin/python
#  This program is using LSTM with Masking to deal with missing values
#  The program is based on the sample program used for illustrating how to write a program in Keras for Vanilla GRU
#

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Masking
from keras.models import model_from_json
import numpy
import datetime
import time
import pandas as pd


import pandas

## SET BACKEND
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt

# (New 1)
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)

def generateTrainDataAndTestData(timeSeriesDataFilename, look_back):
	# to read the data from the file
	dataframe = pandas.read_csv(timeSeriesDataFilename, usecols=[2,3,4,5])
	data_int_TwoDim = dataframe.values
	data_float_TwoDim = data_int_TwoDim.astype(float)
	
	# to perform the normalization (New 1)
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaler = scaler.fit(data_float_TwoDim)
	data_float_TwoDim = scaler.transform(data_float_TwoDim)
	
	# to save the scaler information into a file (New 1)
	scaler_filename = "scaler.save"
	joblib.dump(scaler, scaler_filename) 
	
	# to split the data into the training set and the test set
	data_size = len(data_float_TwoDim)
	train_size = int(data_size*0.80)
	test_size = data_size - train_size
	
	# to generate the training set and the test set
	trainData = data_float_TwoDim[0:train_size, :]
	testData = data_float_TwoDim[train_size:data_size, :]
	trainDataX, trainDataY = create_dataset(trainData, look_back)
	testDataX, testDataY = create_dataset(testData, look_back)
	
	return data_float_TwoDim, trainDataX, trainDataY, testDataX, testDataY

# to preprocess the time series data to generate the correct format of
# the input data for the model (for the new data)
def generateNewData(newTimeSeriesNoOutputDataFilename, look_back):
    # to read the data from the file
    dataframe = pandas.read_csv(newTimeSeriesNoOutputDataFilename, usecols=[2,3,4,5])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)
    # to read the scaler information from a file (New 1)
    scaler_filename = "scalerLSTM.save"
    scaler = joblib.load(scaler_filename)
    # to perform the normalization (New 1)
    data_float_TwoDim = scaler.transform(data_float_TwoDim)
    # to generate the new set
    newDataX, newDataY = create_dataset(data_float_TwoDim, look_back)
    # we ignore newDataY here (since we want to create a new dataset
    # for the model to do the prediction
    return newDataX

# to train a model
def trainModel(trainDataX, trainDataY, testDataX, testDataY, look_back):
    numpy.random.seed(int(time.time()))
    model = Sequential()
    print(trainDataX.shape)
    print(trainDataY.shape)
    print(testDataX.shape)
    print(testDataY.shape)
    model.add(Masking(mask_value=-1,input_shape=(4,1)))
    model.add(LSTM(3, return_sequences=True, input_shape=(4,4)))
    model.add(LSTM(2))
    model.add(Dense(1, activation='relu'))
    # Step 3: to compile the model
    print("  Step 3: to compile the model...")
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])# sample program example
    # model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=["mean_squared_error"])# sample program example
    # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    #Based on comments from "https://www.reddit.com/r/MachineLearning/comments/3i6fp9/what_optimization_methods_work_best_for_lstms/", we can try to use rmsprop, sgd
    #If we encounter a sudden drop in accuracy like what is discussed in "https://github.com/keras-team/keras/issues/3425", use adam or rmsprop but not sgd
    # Step 4: To fit the model
    print("  Step 4: to fit the model...")
    #model.fit(numpyX, numpyY, validation_split=0.2, epochs=1000, batch_size=1)	#sample program example
    model.fit(trainDataX, trainDataY, validation_split=0.2, epochs=200, batch_size=2)
    # model.fit(numpyX, numpyY, validation_split=0.2, epochs=1000, batch_size=1)	#default setting for batch size; the batch size can be updated
    # Step 5: To evaluate the model
    print("  Step 5: to evaluate the model...")
    trainScores = model.evaluate(trainDataX, trainDataY)
    testScores = model.evaluate(testDataX, testDataY)
    print("")
    print("{}: {}".format(model.metrics_names[1], trainScores[1]))
    print("{}: {}".format(model.metrics_names[1], testScores[1]))
    return model

# to save a model
def saveModel(model, modelFilenamePrefix):
    # Step 1: to save the model structure to a file in the JSON format
    print("  Step 1: to save the model structure to a file in the JSON format...")
    structureFilename = modelFilenamePrefix + ".json"
    model_json = model.to_json()
    with open(structureFilename, "w") as f:
        f.write(model_json)
    # Step 2: to save the model weight information to a file in the HDF5 format
    print("  Step 2: to save the model weight information to a file in the HDF5 format...")
    weightFilename = modelFilenamePrefix + ".h5"
    model.save_weights(weightFilename)

# to read a model
def readModel(modelFilenamePrefix):
    # Step 1: to load the model structure from a file in the JSON format
    print("  Step 1: to load the model structure from a file in the JSON format...")
    structureFilename = modelFilenamePrefix + ".json"
    with open(structureFilename, "r") as f:
        model_json = f.read()
    model = model_from_json(model_json)

    # Step 2: to load the model weight information from a file in the HDF5 format
    print("  Step 2: to load the model weight information from a file in the HDF5 format...")
    weightFilename = modelFilenamePrefix + ".h5"
    model.load_weights(weightFilename)

    return model

#def plotResult(trainDataY, testDataY, newDataY_TwoDim, look_back):
def deNormalize(newY_Predict, trainDataX, trainDataY, testDataY, data_float_TwoDim, look_back):
    # to re-map the normalized values to the original values (New 1)
    scaler_filename = "scaler.save"
    scaler = joblib.load(scaler_filename)
    print(newY_Predict.shape, trainDataX.shape, trainDataY.shape)
    # data_float_TwoDim (New 1)
    data_float_TwoDim = scaler.inverse_transform(data_float_TwoDim)
    # newY_Predict (New 1)
    print(newY_Predict)
    newY_Predict = newY_Predict.reshape(len(newY_Predict), 1)
    newY_Predict = scaler.inverse_transform(newY_Predict)
    newY_Predict = newY_Predict.reshape(len(newY_Predict))

    # trainDataY (New 1)
    trainDataY_TwoDim = trainDataY.reshape(len(trainDataY), 1)
    trainDataY_TwoDim = scaler.inverse_transform(trainDataY_TwoDim)
    trainDataY = trainDataY_TwoDim.reshape(len(trainDataY_TwoDim))
    # testDataY (New 1)
    testDataY_TwoDim = testDataY.reshape(len(testDataY), 1)
    testDataY_TwoDim = scaler.inverse_transform(testDataY_TwoDim)
    testDataY = testDataY_TwoDim.reshape(len(testDataY_TwoDim))
    # newY_TwoDim (New 1)
    newY_TwoDim = scaler.inverse_transform(newY_TwoDim)
    # to re-shape "data_float_TwoDim" from 2 dimensions to 1 dimension
    data_size = len(data_float_TwoDim)
    data_float_OneDim = data_float_TwoDim.reshape(data_size)
    newY_OneDim = newY_TwoDim.reshape(data_size-look_back)
    # to find the train_size
    train_size = int(data_size*0.80)
    test_size = data_size - train_size
    return trainDataX, trainDataY, newY_Predict

# to predict the target attribute of a new dataset (in our case, the content from the training set) based on a model
# In our case, the new dataset comes from the variable numpyX
def predictNewDatasetFromModel(trainDataX, trainDataY, data_float_TwoDim, testDataY, newTargetAttributeDataFilename, model, look_back):
    # Step 1: to load the new data (input attributes)
    print("  Step 1: to load the new data...")
    # This could be found in variable numpyX
    # Step 2: to predict the target attribute of the new data based on a model
    print("  Step 2: Step 2: to predict the target attribute of the new data based on a model...")
    newY_Predict = model.predict(trainDataX, batch_size=1)
    # Step 3: to save the predicted target attribute of the new data into a file
    print("  Step 3: to save the predicted target attribute of the new data into a file...")
    newY_Predict, trainDataX, trainDataY = deNormalize(newY_Predict, trainDataX, trainDataY, testDataY, data_float_TwoDim, look_back)
    numpy.savetxt(newTargetAttributeDataFilename, newY_Predict, delimiter=",", fmt="%.10f")
    # Step 4 (Extra Step): to show the expected result and the predicted result
    print(trainDataX.shape, trainDataY.shape, newY_Predict.shape)
    #for i in range(len(trainDataX)):
    for i in range(4):
        print("Expected", trainDataY[i], "Predicted", newY_Predict[i, 0])
    return newY_Predict
    #"newY_Predict" previously known as "newY_TwoDim"

def predictionHandler(courseCode,lectureNumber, timeslot):
        # the training dataset is hard-coded in this program
    df = pd.read_csv("allContinuousData_withPreInput.csv")
    df_row = df[(df['code'] == courseCode)&(df['sectionId']==lectureNumber)&(df['sectionId']==lectureNumber)& (df['recordTime']==timeslot)]
    if (int(df_row['wait'].tolist()[0]) != -1):
        return int(df_row['wait'].tolist()[0])
    numpyX = df_row.values[0][2:5]
    # (i.e., the content of this dataset could be found in this program).
    # the new dataset has the same content as the training set
    modelFilenamePrefix = "NN-Model-"+str(courseCode)
    # Phase 3: to read the model from a file
    print("Phase 3: to read the model from a file...")
    model = readModel(modelFilenamePrefix)
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    return newY_TwoDim[0,0]

def main():
    # the training dataset is hard-coded in this program
    # (i.e., the content of this dataset could be found in this program).
    # the new dataset has the same content as the training set
    trainingDataFile = "COMP4332TrainingData_Continuous.csv"   #newly added
    newTimeSeriesNoOutputDataFilename = trainingDataFile #newly added, to be connected to "main.py"
    newTargetAttributeDataFilename = "New-COMP4332-NN-Output.csv"

    modelFilenamePrefix = "NN-COMP4332-prediction"#newly added

    look_back = 4   #newly added

    # Phase 1: to train the model
    print("Phase 1: to train the model...")
    #Please store the dataset for training into the .csv file called "training.csv""
    data_float_TwoDim, trainDataX, trainDataY, testDataX, testDataY = generateTrainDataAndTestData(trainingDataFile, look_back)

    newDataX = generateNewData(newTimeSeriesNoOutputDataFilename, look_back)

    print("data_float_TwoDim: ")
    print(data_float_TwoDim)
    print("trainDataX: ")
    print(trainDataX)
    print("trainDataY: ")
    print(trainDataY)
    print("testDataX: ")
    print(testDataX)
    print("testDataY: ")
    print(testDataY)
    print("newDataX: ")
    print(newDataX)

    model = trainModel(trainDataX, trainDataY, testDataX, testDataY, look_back)
    # Phase 2: to save the model to a file
    print("Phase 2: to save the model to a file...")
    saveModel(model, modelFilenamePrefix)
    # Phase 3: to read the model from a file
    print("Phase 3: to read the model from a file...")
    model = readModel(modelFilenamePrefix)
    # Phase 4: to predict the target attribute of a new dataset based on a model
    print("Phase 4: to predict the target attribute of a new dataset based on a model...")
    #predictNewDatasetFromModel(numpyX, numpyY, newTargetAttributeDataFilename, model)
    predictedDataY = predictNewDatasetFromModel(trainDataX, trainDataY, data_float_TwoDim, testDataY, newTargetAttributeDataFilename, model, look_back)