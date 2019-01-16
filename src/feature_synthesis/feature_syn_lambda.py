import featuretools as ft
import pandas as pd
import utils, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

es = utils.load_entityset("./featuretools_part_1/")
print (es)
label_times = utils.make_labels(es=es,
                                product_name = "Banana",
                                cutoff_time = pd.Timestamp('March 15, 2015'),
                                prediction_window = ft.Timedelta("4 weeks"),
                                training_window = ft.Timedelta("60 days"))

feature_matrix, features = ft.dfs(target_entity="users", 
                                  cutoff_time=label_times,
                                  training_window=ft.Timedelta("60 days"), # same as above
                                  entityset=es,
                                  verbose=True)

# Encode categorical values
fm_encoded, features_encoded = ft.encode_features(feature_matrix, features)

print("Number of features %s" % len(features_encoded))
print(features_encoded)

# Sample the feature by user input


# Train the classifier

