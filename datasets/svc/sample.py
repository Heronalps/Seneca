import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("./datasets/neural_network/df_2017_reduced.csv")
df_train = df.iloc[:, 0 : -1]
scaler = StandardScaler()
scaler.fit(df_train)
df_train = scaler.transform(df_train)
df.iloc[:, 0:-1] = df_train
df.to_csv('./datasets/svc/df_2017_reduced_scaler.csv', index=False)