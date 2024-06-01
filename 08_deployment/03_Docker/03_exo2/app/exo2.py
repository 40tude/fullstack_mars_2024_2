import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from joblib import dump
import os

# Import dataset
df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")

# X, y split 
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Train / test split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# Pipeline 
model = Pipeline(steps=[
    ("standard_scaler", StandardScaler()),
    ("Regressor",RandomForestRegressor(n_estimators=30, min_samples_split=5))
])

model.fit(X_train, y_train)

# Print Scores 
print(f"Train score: {model.score(X_train, y_train)}")
print(f"Test score: {model.score(X_test, y_test)}")

# Persist our model 
print("Saving model...")
dump(model, "house_prices_model.joblib")
print(f"Model has been saved here: {os.getcwd()}")