import numpy as np
import pandas as pd

csv = r"F:\pycharm_workspce\dai_github\machine_learning\NLP\seq2seq\reviews.csv"

df = pd.read_csv(csv)

print(df.head(10))
# 检查null
print(df.isnull().sum())
# 移除null
cleanedDF = df.dropna()
print("移除null:\n", cleanedDF.isnull().sum())
# 取出指定的列
df = cleanedDF.drop(
    labels=['Id', 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator', 'HelpfulnessDenominator',
            'Score', 'Time'], axis=1)
print(df.head())
# print(df.iloc[0,1])
# print(df.iloc[0,0])

