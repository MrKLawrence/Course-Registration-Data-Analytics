#!/usr/bin/python
#
#  The program was written by 
#  The program is based on the sample program used for illustrating how to write a program in Keras for Vanilla GRU
#

from keras.models import Sequential
from keras.layers import GRU
from keras.layers import Dense
from keras.models import model_from_json
import numpy

# to train a model
def trainModel(trainingfile):
	# to set the "fixed" seed of a random number generator used in the "optimization" tool
	# in the neural network model
	# The reason why we fix this is to reproduce the same output each time we execute this program
	# In practice, you could set it to any number (or, the current time) (e.g., "numpy.random.seed(int(time.time()))")
	#numpy.random.seed(117)	#sample program example
	numpy.random.seed(int(time.time()))
	#Fetch data from dataset
	data = numpy.loadtxt(trainingfile, dtype='float, float, U3', delimiter=',')	#please update the correct form of data {code,sections.sectionId,sections.quota,sections.enrol,sections.wait,sections.recordTime} with correct data types
	for i in data:
	    temp = []
	    temp.append(i[0])
	    temp.append(i[1])
	    if i[2] == 'Yes':
	        temp.append(1)
	    else:
	        temp.append(0)
	    training.append(temp)
	# the training data
	X = numpy.array(training)[:,0:2]
	Y = numpy.array(training)[:,2]
	print("Training Data: ")
	print("X's shape:", X.shape)
	print("Y's shape:", Y.shape)
	# Step 1: to load the data
	print("  Step 1: to load the data...")
	# the datasets are stored in variables pythonX and pythonY	
	# Step 2: to define the model
	print("  Step 2: to define the model...")
	model = Sequential()
	model.add(GRU(1, input_shape=(3, 2)))
	#model.add(Dense(1, activation='relu'))	#sample program example
	model.add(Dense(1, activation='sigmoid'))
	#model.add(Dense(1, activation='tanh'))	#alternative
	# Step 3: to compile the model
	print("  Step 3: to compile the model...")	
	#model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])# sample program example
	model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=["mean_squared_error"])# sample program example
	#Based on comments from "https://www.reddit.com/r/MachineLearning/comments/3i6fp9/what_optimization_methods_work_best_for_lstms/", we can try to use rmsprop, sgd
	#If we encounter a sudden drop in accuracy like what is discussed in "https://github.com/keras-team/keras/issues/3425", use adam or rmsprop but not sgd
	# Step 4: To fit the model
	print("  Step 4: to fit the model...")
	#model.fit(numpyX, numpyY, validation_split=0.2, epochs=1000, batch_size=1)	#sample program example
	model.fit(X, Y, validation_split=0.2, epochs=1000, batch_size=1)	#default setting for batch size; the batch size can be updated
	# Step 5: To evaluate the model
	print("  Step 5: to evaluate the model...")
	scores = model.evaluate(X, Y)
	print("")
	print("{}: {}".format(model.metrics_names[1], scores[1]))
	return X, Y, model

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

# to predict the target attribute of a new dataset (in our case, the content from the training set) based on a model	
# In our case, the new dataset comes from the variable numpyX
def predictNewDatasetFromModel(numpyX, numpyY, newTargetAttributeDataFilename, model):
	# Step 1: to load the new data (input attributes)
	print("  Step 1: to load the new data...")
	# This could be found in variable numpyX
	# Step 2: to predict the target attribute of the new data based on a model
	print("  Step 2: Step 2: to predict the target attribute of the new data based on a model...")
	newY_TwoDim = model.predict(numpyX, batch_size=1)
	# Step 3: to save the predicted target attribute of the new data into a file
	print("  Step 3: to save the predicted target attribute of the new data into a file...")
	numpy.savetxt(newTargetAttributeDataFilename, newY_TwoDim, delimiter=",", fmt="%.10f")
	# Step 4 (Extra Step): to show the expected result and the predicted result
	for i in range(len(numpyX)):
		print("Expected", numpyY[i, 0], "Predicted", newY_TwoDim[i, 0])

def main():
	# the training dataset is hard-coded in this program
	# (i.e., the content of this dataset could be found in this program).
	# the new dataset has the same content as the training set
	newTargetAttributeDataFilename = "New-GRU-Output.csv"
	modelFilenamePrefix = "GRU-Model"
	# Phase 1: to train the model
	print("Phase 1: to train the model...")
	#Please store the dataset for training into the .csv file called "training.csv""
	numpyX, numpyY, model = trainModel('training.csv')
	# Phase 2: to save the model to a file
	print("Phase 2: to save the model to a file...")
	saveModel(model, modelFilenamePrefix)
	# Phase 3: to read the model from a file
	print("Phase 3: to read the model from a file...")
	model = readModel(modelFilenamePrefix)	
	# Phase 4: to predict the target attribute of a new dataset based on a model
	print("Phase 4: to predict the target attribute of a new dataset based on a model...")
	predictNewDatasetFromModel(numpyX, numpyY, newTargetAttributeDataFilename, model)
	
main()