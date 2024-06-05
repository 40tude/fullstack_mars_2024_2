FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN pip install altair pandas numpy streamlit pydeck

# On ne fait pas de copie quand on est en test local sous WIN11
COPY . /home/app

CMD streamlit run --server.port $PORT app.py