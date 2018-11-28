### Read data from csv-file and returns data as Numpy array (N-dimensional according to number of columns in file)
def getInputData(inputFile):
    data = np.genfromtxt(inputFile, delimiter = ",")
    return data