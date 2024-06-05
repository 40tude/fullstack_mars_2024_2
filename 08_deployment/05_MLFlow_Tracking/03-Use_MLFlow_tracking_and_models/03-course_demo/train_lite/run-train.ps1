# Faut penser à faire tourner secrets.ps1 pour définir APP_URI, AWS_ACCESS_KEY_ID et AWS_SECRET_ACCESS_KEY

# docker run -it `
#  -p 4000:4000 `
#  -v "$(pwd):/home/app" `
#  -e APP_URI=${Env:APP_URI} `
#  -e AWS_ACCESS_KEY_ID=${Env:AWS_ACCESS_KEY_ID} `
#  -e AWS_SECRET_ACCESS_KEY=${Env:AWS_SECRET_ACCESS_KEY} `
#  sample-mlflow-server python train.py



#  -p 4000:4000 `
#  -v "$(pwd):/home/app" `

 docker run -it `
 -e APP_URI=${Env:APP_URI} `
 sample-mlflow-server python train.py