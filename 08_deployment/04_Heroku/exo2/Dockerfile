FROM continuumio/miniconda3

WORKDIR /home/app

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip install --requirement /tmp/requirements.txt

COPY ./app /home/app

CMD streamlit run --server.port $PORT exo2.py