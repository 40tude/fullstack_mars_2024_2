import argparse
import os
import pandas as pd
import time
import mlflow  # Ver 1.5 supports autolog with 0.24.1 <= scikit-learn <= 1.4.2

# import sklearn
from mlflow.models.signature import infer_signature

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


if __name__ == "__main__":
    # print("sklearn : ", sklearn.__version__)
    # print("mlflow  : ", mlflow.__version__)

    # Set your variables for your environment
    EXPERIMENT_NAME = "appointment_cancellation_detector"

    # Set tracking URI to your Heroku application
    mlflow.set_tracking_uri(os.environ["APP_URI"])

    # Set experiment's info
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    ### MLFLOW Experiment setup
    # experiment_name="appointment_cancellation_detector"
    # mlflow.set_experiment(experiment_name)
    # experiment = mlflow.get_experiment_by_name(experiment_name)

    # client = mlflow.tracking.MlflowClient()
    # mlflow.set_tracking_uri(os.environ["APP_URI"])

    # run = client.create_run(experiment.experiment_id)

    print("training model...")

    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)  # We won't log models right away

    # Parse arguments given in shell script
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", default=1)
    parser.add_argument("--min_samples_split", default=2)
    args = parser.parse_args()

    # Import dataset
    df = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/doctolib_simplified_dataset_01.csv"
    )

    df = df.head(1_000)
    print(df.shape)

    # X, y split
    X = df.iloc[:, 3:-1]
    y = df.iloc[:, -1].apply(lambda x: 0 if x == "No" else 1)

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print(df.columns)

    # Preprocessing
    def date_processing(df):
        df = df.copy()

        ## Transform datetime into a number
        # df["ScheduledDay"] = pd.to_datetime(
        #     df["ScheduledDay"], yearfirst=True, infer_datetime_format=True
        # )
        df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], yearfirst=True)

        # df["AppointmentDay"] = pd.to_datetime(
        #     df["AppointmentDay"], yearfirst=True, infer_datetime_format=True
        # )
        df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], yearfirst=True)

        ## Get the difference between scheduled day and appointment
        df["time_difference_between_scheduled_and_appointment"] = (
            df["AppointmentDay"] - df["ScheduledDay"]
        ).dt.days

        ## Remove redundant info
        df = df.drop(["ScheduledDay", "AppointmentDay"], axis=1)

        return df

    date_preprocessor = FunctionTransformer(date_processing)

    # Preprocessing
    print("Preprocessing...")

    X_train_after_date_processing = date_processing(X_train)
    categorical_features = X_train_after_date_processing.select_dtypes(
        "object"
    ).columns  # Select all the columns containing strings
    categorical_transformer = OneHotEncoder(
        drop="first", handle_unknown="error"
    )  # , sparse=False)

    numerical_feature_mask = ~X_train_after_date_processing.columns.isin(
        X_train_after_date_processing.select_dtypes("object").columns
    )  # Select all the columns containing anything else than strings
    numerical_features = X_train_after_date_processing.columns[numerical_feature_mask]
    numerical_transformer = StandardScaler()

    feature_preprocessor = ColumnTransformer(
        transformers=[
            ("categorical_transformer", categorical_transformer, categorical_features),
            ("numerical_transformer", numerical_transformer, numerical_features),
        ]
    )

    # Pipeline
    print("Pipeline...")

    n_estimators = int(args.n_estimators)
    min_samples_split = int(args.min_samples_split)

    model = Pipeline(
        steps=[
            ("Dates_preprocessing", date_preprocessor),
            ("features_preprocessing", feature_preprocessor),
            (
                "Regressor",
                RandomForestClassifier(
                    n_estimators=n_estimators, min_samples_split=min_samples_split
                ),
            ),
        ]
    )

    # Log experiment to MLFlow
    print("Log experiment to MLFlow...")
    with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
        print("Après mlflow.start_run...")
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup
        print("Avant mlflow.sklearn.log_model...")
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="appointment_cancellation_detector",
            registered_model_name="appointment_cancellation_detector_RF",
            signature=infer_signature(X_train, predictions),
        )
        print("Après mlflow.sklearn.log_model...")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
