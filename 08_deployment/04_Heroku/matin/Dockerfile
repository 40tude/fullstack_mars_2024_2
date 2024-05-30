# anaconda lite
FROM continuumio/miniconda3

WORKDIR /home/app

# RUN apt-get update
# RUN apt-get install nano unzip
# RUN apt install curl -y

# RUN curl -fsSL https://get.deta.dev/cli.sh | sh
# RUN pip install boto3 pandas gunicorn streamlit sklearn matplotlib seaborn plotly
RUN pip install pandas streamlit plotly
COPY . /home/app

# C'est heroku qui va fournir le port 
CMD streamlit run --server.port $PORT app.py

