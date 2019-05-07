#model5
#!/usr/bin/python
#
#  The program is based on the sample program used for illustrating how to write a program in Keras for Vanilla GRU
#

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import model_from_json

import datetime
import time
import numpy
import pandas

from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib

def create_dataset(dataset):
    look_back = 2
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), :]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 3])
    numpyX = numpy.array(dataX)
    numpyY = numpy.array(dataY)
    numpyX = numpyX.reshape(len(numpyX), 8)
    numpyY = numpyY[:,numpy.newaxis]
    return numpyX,numpyY

# to preprocess the time series data to generate the correct format of
# the input data for the model (for the training data and the test data)
def generateTrainDataAndTestData(timeSeriesDataFilename, prefix):
    # to read the data from the file
    dataframe = pandas.read_csv(timeSeriesDataFilename, usecols=[2,3,4,5])
    data_int_TwoDim = dataframe.values
    data_float_TwoDim = data_int_TwoDim.astype(float)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(data_float_TwoDim)
    data_float_TwoDim = scaler.transform(data_float_TwoDim)
    # print("data_float_TwoDim")
    # print(data_float_TwoDim)
    # to save the scaler information into a file (New 1)
    scaler_filename = prefix+"scaler.save"
    joblib.dump(scaler, scaler_filename)
    dataframe = pandas.DataFrame(data_float_TwoDim)
    randomMask = numpy.random.rand(len(dataframe)) < 0.8
    trainData = dataframe[randomMask].values.astype(float)
    testData = dataframe[~randomMask].values.astype(float)
    trainDataX, trainDataY = create_dataset(trainData)
    testDataX, testDataY = create_dataset(testData)
    return trainDataX, trainDataY, testDataX, testDataY

# to train a model
def trainModel(trainDataX, trainDataY):
    numpy.random.seed(int(time.time()))
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Step 3: to compile the model
    print("  Step 3: to compile the model...")
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error", "accuracy"])# sample program example
    # model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=["mean_squared_error"])# sample program example
    # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    #Based on comments from "https://www.reddit.com/r/MachineLearning/comments/3i6fp9/what_optimization_methods_work_best_for_lstms/", we can try to use rmsprop, sgd
    #If we encounter a sudden drop in accuracy like what is discussed in "https://github.com/keras-team/keras/issues/3425", use adam or rmsprop but not sgd
    # Step 4: To fit the model
    print("  Step 4: to fit the model...")
    model.fit(trainDataX, trainDataY, validation_split=0.2, epochs=500, batch_size=20)
    # Step 5: To evaluate the model
    print("  Step 5: to evaluate the model...")
    trainScores = model.evaluate(trainDataX, trainDataY)
    # testScores = model.evaluate(testDataX, testDataY)
    print("")
    print("{}: {}".format(model.metrics_names[1], trainScores[1]))
    # print("{}: {}".format(model.metrics_names[1], testScores[1]))
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

def deNormalize(testDataX, testDataY, prefix=""):
    scaler_filename = str(prefix)+"scaler.save"
    scaler = joblib.load(scaler_filename)
    tempData = numpy.hstack((testDataX[:,:3],testDataY))
    testDataY = scaler.inverse_transform(tempData)
    testDataY = testDataY[:,3:]
    length = int(len(testDataX)*2)
    testDataX = testDataX.reshape(length,4)
    testDataX= scaler.inverse_transform(testDataX)
    length = int(len(testDataX)/2)
    testDataX = testDataX.reshape(length,8)
    return testDataX, testDataY

# to predict the target attribute of a new dataset (in our case, the content from the training set) based on a model
# In our case, the new dataset comes from the variable numpyX
def predictNewDatasetFromModel( testDataX, testDataY, newTargetAttributeDataFilename,prefix, model):
    # Step 1: to load the new data (input attributes)
    print("  Step 1: to load the new data...")
    # This could be found in variable numpyX
    # Step 2: to predict the target attribute of the new data based on a model
    print("  Step 2: Step 2: to predict the target attribute of the new data based on a model...")
    newY_Predict = model.predict(testDataX, batch_size=1)
    # Step 3: to save the predicted target attribute of the new data into a file
    print("  Step 3: to save the predicted target attribute of the new data into a file...")
    # newY_Predict, trainDataX, trainDataY = deNormalize(newY_Predict, trainDataX, trainDataY, testDataY, data_float_TwoDim, look_back)
    testDataX, newY_Predict = deNormalize(testDataX, newY_Predict, prefix)
    testDataX, testDataY = deNormalize(testDataX, testDataY, prefix)

    numpy.savetxt(newTargetAttributeDataFilename, newY_Predict, delimiter=",", fmt="%.10f")
    # Step 4 (Extra Step): to show the expected result and the predicted result
    print(testDataY.shape, newY_Predict.shape)
    #for i in range(len(trainDataX)):
    for i in range(len(testDataY)):
        print("Expected", testDataY[i], "Predicted", newY_Predict[i, 0])
    print("12,8relu,1sigmoid,loss=mean_squared_error, optimizer=adam,epoch=500,batch=20")
    return newY_Predict
    #"newY_Predict" previously known as "newY_TwoDim"

def predictionHandler(courseCode,lectureNumber, timeslot):
        # the training dataset is hard-coded in this program
    df = pandas.read_csv("allContinuousData_withPreInput.csv")
    df_row = df[(df['code'] == courseCode)&(df['sectionId']==lectureNumber)&(df['sectionId']==lectureNumber)& (df['recordTime']==timeslot)]
    if (int(df_row['wait'].tolist()[0]) != -1):
        return int(df_row['wait'].tolist()[0])
    while True:
        timeslot -= 1
        df_row = df[(df['code'] == courseCode)&(df['sectionId']==lectureNumber)&(df['sectionId']==lectureNumber)& (df['recordTime']==timeslot)]
        if (int(df_row['wait'].tolist()[0]) != -1):
            break
    numpyX1 = df_row.values[0][2:6]
    while True:
        timeslot -= 1
        df_row = df[(df['code'] == courseCode)&(df['sectionId']==lectureNumber)&(df['sectionId']==lectureNumber)& (df['recordTime']==timeslot)]
        if (int(df_row['wait'].tolist()[0]) != -1):
            break
    numpyX2 = df_row.values[0][2:6]
    scaler_filename = str(courseCode)+"scaler.save"
    scaler = joblib.load(scaler_filename)
    numpyX1 = scaler.transform(numpy.reshape(numpyX1, (1, 4)))
    numpyX2 = scaler.transform(numpy.reshape(numpyX2, (1, 4)))
    numpyX = numpy.hstack((numpyX2,numpyX1))
    modelFilenamePrefix = str(courseCode)+"-Prediction-Model"
    print("Phase 3: to read the model from a file...")
    model = readModel(modelFilenamePrefix)
    newY_TwoDim = model.predict(numpyX, batch_size=1)
    X, newY_TwoDim = deNormalize(numpyX, newY_TwoDim, courseCode)
    return newY_TwoDim[0,0]

def main():
    #coursesListForPredict = ["COMP1942"]
    #coursesListForPredict = ["COMP4332"]
    #coursesListForPredict = ["RMBI4310"]
    coursesListForPredict = ["COMP1942","COMP4211","COMP4221","COMP4321","COMP4331","COMP4332","RMBI1010","RMBI3000A","RMBI4210","RMBI4310"]
    for prefix in coursesListForPredict:
        trainingDataFile = prefix + "TrainingData.csv"   #newly added
        # newTimeSeriesNoOutputDataFilename = trainingDataFile #newly added, to be connected to "main.py"
        newTargetAttributeDataFilename = prefix+"New-Prediction-Output.csv"
        modelFilenamePrefix = prefix+"-Prediction-model"#newly added
        print("Phase 1: to train the model...")
        #Please store the dataset for training into the .csv file called "training.csv""
        trainDataX, trainDataY, testDataX, testDataY = generateTrainDataAndTestData(trainingDataFile,prefix)
        model = trainModel(trainDataX, trainDataY)
        print("  Step 5: to evaluate the model...")
        testScores = model.evaluate(testDataX, testDataY)
        print("")
        print("{}: {}".format(model.metrics_names[1], testScores[1]))
        # Phase 2: to save the model to a file
        print("Phase 2: to save the model to a file...")
        saveModel(model, modelFilenamePrefix)
        # Phase 3: to read the model from a file
        print("Phase 3: to read the model from a file...")
        model = readModel(modelFilenamePrefix)
        # Phase 4: to predict the target attribute of a new dataset based on a model
        print("Phase 4: to predict the target attribute of a new dataset based on a model...")
        #predictNewDatasetFromModel(numpyX, numpyY, newTargetAttributeDataFilename, model)
        # predictedDataY = predictNewDatasetFromModel(trainDataX, trainDataY, testDataX, testDataY,data_float_TwoDim, newTargetAttributeDataFilename, model, look_back)
        predictNewDatasetFromModel( testDataX, testDataY, newTargetAttributeDataFilename, prefix, model)
# x=predictionHandler("COMP1942",1,287)
# print(x)
# 287,135,135
#main()