import os
import mlflow
from mlflow import log_metric, log_param, log_artifacts
from random import random, randint

# Set tracking URI to your Heroku application
print("Debug : APP_URI = ", os.environ["APP_URI"])
mlflow.set_tracking_uri(os.environ["APP_URI"])

if __name__ == "__main__":
    # Log a parameter (key-value pair)
    log_param("param1", randint(0, 100))

    # Log a metric; metrics can be updated throughout the run
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    # Log an artifact (output file)
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")
    log_artifacts("outputs")
