# docker run -it -v "$(pwd):/home/app" jedha/slim-machine-learning-image

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler #, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
import pickle as pkl

print("Chemin de VSCode           : ", Path.cwd())
p = Path(__file__).parent
print("Chemin contenant le script : ", p)

# df = pd.read_csv(p/"california_housing_market.csv")
df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
print(df.head())

print(df.shape)
print(df.describe(include="all").T)
print(df.info())
print(100 * df.isnull().sum() / df.shape[0])

target_name = "MedHouseVal"
X = df.drop(columns = target_name)
y = df[target_name]

numeric_features     = df.select_dtypes(include="number").columns
categorical_features = df.select_dtypes(exclude="number").columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) # , stratify = y

numeric_transformer = Pipeline(
  steps=[
    ("imputer_num", SimpleImputer(strategy="median")),
    ("scaler_num" , StandardScaler()),
  ]
)

# categorical_transformer = Pipeline(
#   steps=[
#     ("imputer_cat", SimpleImputer(strategy="most_frequent")),  
#     ("encoder_cat", OneHotEncoder(drop="first")),                 
#   ]
# )

preprocessor = ColumnTransformer(
  transformers=[
    ("num", numeric_transformer,     numeric_features),
    # ("cat", categorical_transformer, categorical_features),
  ]
)

model = LinearRegression()
model.fit(X_train, y_train) 

y_train_pred = model.predict(X_train)
print(y_train_pred[0:5])

y_test_pred = model.predict(X_test)
print(y_test_pred[0:5])
print(model.score(X_train, y_train))
print(model.score(X_test,  y_test))

with open(p/"my_model.pickle", "wb") as output_file:
  pkl.dump(model, output_file)

with open(p/"my_model.pickle", "rb") as input_file:
  model2 = pkl.load(input_file)

print(model.predict(X[0:1]))
print(model2.predict(X[0:1]))



