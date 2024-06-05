docker run -it\
 -p 4000:4000\
 -v "$(pwd):/home/app"\
 -e APP_URI="APP_URI"\
 -e AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"\
 -e AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"\
 sample-mlflow-server python train.py --n_estimators=100 --min_samples_split=2