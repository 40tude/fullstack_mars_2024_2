import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler     
from sklearn.compose import ColumnTransformer

from xgboost import XGBClassifier 

k_target        = "converted"
k_samples_ratio = 100/100   # percentage of observation to be taken into account. Pass 100/100 for final testing 
k_test_size     = 20/100    # see train_test_split
k_random_state  = 42        # you know why...
header          = "conversion_data_test_predictions_"
author          = "PHILIPPE"

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Entrainement classique 

df = pd.read_csv('./assets/conversion_data_train.csv')
df.head()


X = df.drop(columns = k_target)
y = df[k_target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=k_test_size, random_state=k_random_state, stratify = y)



numeric_transformer = Pipeline(
  steps=[
    ("scaler_num", StandardScaler()),
  ]
)

categorical_transformer = Pipeline(
  steps=[
    ("encoder_cat", OneHotEncoder(drop="first")),                 
  ]
)

numeric_features      = X.select_dtypes(include="number").columns
categorical_features  = X.select_dtypes(exclude="number").columns

preprocessor = ColumnTransformer(
  transformers=[
    ("num", numeric_transformer,     numeric_features),
    ("cat", categorical_transformer, categorical_features),
  ]
)

X_train = preprocessor.fit_transform(X_train)
X_test  = preprocessor.transform(X_test)

# print(X_train[0:5].round(3))
# print(X_train.shape)
# print(type(X_train))

# param_grid = {
#     'learning_rate'     : [0.05, 0.1],  # ralenti grid search CV si petit
#     'n_estimators'      : [200, 300],
#     'max_depth'         : [5, 3],
#     'subsample'         : [0.9, 0.8],
#     'colsample_bytree'  : [0.9, 0.8],
#     'scale_pos_weight'  : [30, 20] 
# }

# Pas touche!
param_grid = {
    'learning_rate'     : [0.01, 0.1],
    'n_estimators'      : [100, 200],
    'max_depth'         : [5, 3],
    'subsample'         : [0.9, 0.8],
    'colsample_bytree'  : [0.9, 0.8],
    'scale_pos_weight'  : [10, 1] 
}

# https://machinelearningmastery.com/xgboost-for-imbalanced-classification/
# param_grid = {
#     'learning_rate'       : [0.01, 0.05, 0.1],
#     'n_estimators'        : [200, 400, 600],
#     'max_depth'           : [6, 8, 10],
#     'subsample'           : [0.8, 0.9, 1.0],
#     'colsample_bytree'    : [0.8, 0.9, 1.0],
#     'scale_pos_weight'    : [10, 20, 30]  # Control the balance of positive and negative weights, useful for unbalanced classes. 
# }                                         # A typical value to consider: sum(negative instances) / sum(positive instances). 

# param_grid = {
#     'learning_rate'       : [0.01, 0.05],
#     'n_estimators'        : [200, 400],
#     'max_depth'           : [6, 8],
#     'subsample'           : [0.8, 0.9],
#     'colsample_bytree'    : [0.8, 0.9],
#     'scale_pos_weight'    : [30, 20]  # Control the balance of positive and negative weights, useful for unbalanced classes. 
# }                                     # A typical value to consider: sum(negative instances) / sum(positive instances). 


xgb = XGBClassifier()

grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, scoring="f1", verbose = 3, n_jobs = -1, cv = 5)    # refit=True by default
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print(best_model)

best_params = grid_search.best_params_
print(best_params)

results = grid_search.cv_results_
df_results = pd.DataFrame(results)
df_results.to_csv('./assets/grid_search_results.csv', index=False)

y_pred = grid_search.predict(X_test)

print(f"f1 \t\t precision \t recall")
print(f"{f1_score(y_test,  y_pred):.6f} \t {precision_score(y_test,  y_pred):.6f} \t {recall_score(y_test,  y_pred):.6f}")







# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ## Entrainement sur l'ensemble du jeu de données 

X_full = df.drop(columns = k_target)
y_full = df[k_target]
X_full = preprocessor.fit_transform(X_full)

clf = XGBClassifier(**best_params)
clf.fit(X_full, y_full)
y_pred = clf.predict(X_full)

print(f"f1 \t\t precision \t recall")
print(f"{f1_score(y_full,  y_pred):.6f} \t {precision_score(y_full,  y_pred):.6f} \t {recall_score(y_full,  y_pred):.6f}")



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ## Predictions sur le jeu sans label

X_no_labels = pd.read_csv('./assets/conversion_data_test.csv')
X_no_labels = preprocessor.transform(X_no_labels)
y_no_labels = clf.predict(X_no_labels) 

data = {
  'converted': y_no_labels
}

Y_predictions = pd.DataFrame(columns=['converted'], data=data)

trailer   = datetime.now().strftime("%Y%m%d_%H%M%S")
out_file  = "./assets/" + header + author + "-" + trailer + ".csv"
Y_predictions.to_csv(out_file, index=False)

















#------------------------------------------------------------------------------
# Si je souhaite insérer une fonction (ou une classe ) dans un pipeline de traitement, comment dois je l'écrire ?

# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import FunctionTransformer

# # Définir la fonction à insérer dans le pipeline
# def custom_function(X):
#     # Faire quelque chose avec X
#     # Par exemple, ajouter 1 à chaque valeur
#     return X + 1

# # Créer un pipeline avec la fonction encapsulée dans FunctionTransformer
# pipeline = Pipeline([
#     ('custom_transformer', FunctionTransformer(custom_function))
# ])

# # Utiliser le pipeline sur les données
# X_transformed = pipeline.fit_transform(X)



#------------------------------------------------------------------------------
# from sklearn.base import BaseEstimator, TransformerMixin

# class CustomTransformer(BaseEstimator, TransformerMixin):
#     def __init__(self, parameter1, parameter2):
#         self.parameter1 = parameter1
#         self.parameter2 = parameter2

#     def fit(self, X, y=None):
#         # Réaliser des opérations d'initialisation ou d'apprentissage ici
#         return self

#     def transform(self, X):
#         # Réaliser la transformation des données ici
#         transformed_X = X + self.parameter1
#         transformed_X *= self.parameter2
#         return transformed_X

# # Créer un pipeline avec la classe personnalisée
# pipeline = Pipeline([
#     ('custom_transformer', CustomTransformer(parameter1=1, parameter2=2))
# ])

# # Utiliser le pipeline sur les données
# X_transformed = pipeline.fit_transform(X)





#------------------------------------------------------------------------------
# VOIR AUSSI

# # Création du pipeline avec des étapes de prétraitement et un estimateur final
# pipeline = Pipeline([
#     ('preprocessing', CustomTransformer()),  # Transformer personnalisé
#     ('estimator', RandomForestClassifier())  # Estimateur final
# ])

# # Apprentissage sur l'ensemble d'entraînement
# pipeline.fit(X_train, y_train)

# # Prédiction sur l'ensemble de test
# y_pred = pipeline.predict(X_test)




# ## Preprocessing on df

# A faire uniquement sur les données de train
# PAS sur les données de test (validation) ou les données de test jamais vues
# ATTENTION : 
# Il est sans doute préférable de minorer l'influence des observations redontantes

# indices_redondants = [0, 1, 5, 10]  # Exemple d'indices de données redondantes

# # Calculer les poids des échantillons en inversant leur fréquence
# # Pour pondérer à la baisse les échantillons redondants, vous pouvez diviser 1 par le nombre d'occurrences de chaque échantillon
# weights = np.ones(len(y_train))
# for idx in indices_redondants:
#     weights[idx] = 1.0 / indices_redondants.count(idx)

# Créer un objet DMatrix pour les données d'entraînement avec les poids des échantillons
# dtrain = xgb.DMatrix(data=X_train, label=y_train, weight=weights)

# https://xgboost.readthedocs.io/en/stable/parameter.html
# Réutiliser aussi les paramètres issues du GridSearchCV
# params = {
#     'objective': 'binary:logistic',  # pour un problème de classification binaire
#     'eval_metric': 'auc'  # Métrique d'évaluation
# }

# # Entraîner le modèle XGBoost
# model = xgb.train(params=params, dtrain=dtrain, num_boost_round=100)







# Removing outliers
# Uniquement sur les données de train
# PAS sur les données de test (validation) ou les données de test jamais vues

# print(df.shape)

# numeric_columns = df[["age", "total_pages_visited"]]
# print(type(numeric_columns))
# # numeric_columns = ["age	new_user", "total_pages_visited"]

# # 1. Calculez l'IQR pour chaque colonne numérique
# Q1 = numeric_columns.quantile(0.25)
# Q3 = numeric_columns.quantile(0.75)
# IQR = Q3 - Q1

# # 2. Calculez les limites supérieure et inférieure
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR

# # Créez un masque pour identifier les lignes avec des valeurs aberrantes dans les colonnes numériques
# outliers_mask = ((numeric_columns < lower_bound) | (numeric_columns > upper_bound)).any(axis=1)

# # Filtrez les lignes avec des valeurs aberrantes uniquement dans les colonnes numériques
# df = df[~outliers_mask]
# print(df.shape)

# df.head()

# print(f"shape : {df.shape}")

# # df = add_weight_col(df)  

# print(f"shape : {df.shape}")
 

# # On peut ici limiter la taille de df pour aller plus vite par exemple  
# # df = df.sample(int(k_samples_ratio*len(df)))
# # df = df.iloc[:int(k_samples_ratio*len(df))]


