from keras.layers import LSTM
import keras.models
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    file = r"../data/jena_climate_2009_2016.csv"
    data = pd.read_csv(file)
    print(data.head(100).iloc[:,[0,1,2,3,4]])
    print(data.columns)
    temp = data.iloc[:1440, 2]
    plt.plot(range(len(temp)), temp)
    plt.show()