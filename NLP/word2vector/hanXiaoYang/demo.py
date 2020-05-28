import os
import re
import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

import nltk
from nltk.corpus import stopwords

datafile = os.path.join('.','data','label.csv')

if __name__ == '__main__':
    print("hello world!")