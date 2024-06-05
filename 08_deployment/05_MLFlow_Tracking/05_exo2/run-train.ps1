# Faut penser à faire tourner secrets.ps1 pour définir APP_URI, AWS_ACCESS_KEY_ID et AWS_SECRET_ACCESS_KEY

# docker run -it `
# -p 4000:4000 `
# -v "$(pwd):/home/app" `
# -e APP_URI=${Env:APP_URI} `
# -e PORT=4000 `
# -e AWS_ACCESS_KEY_ID=${Env:AWS_ACCESS_KEY_ID} `
# -e AWS_SECRET_ACCESS_KEY=${Env:AWS_SECRET_ACCESS_KEY} `
# sample-mlflow-server python train.py


docker run -it `
 -v "$(pwd):/home/app" `
 -e APP_URI=${Env:APP_URI} `
 -e AWS_ACCESS_KEY_ID=${Env:AWS_ACCESS_KEY_ID} `
 -e AWS_SECRET_ACCESS_KEY=${Env:AWS_SECRET_ACCESS_KEY} `
 sample-mlflow-server python train.py --n_estimators=100 --min_samples_split=2

#  -p 4000:4000 `





