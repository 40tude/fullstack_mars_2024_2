# A partir du répertoire exo1 où se trouve Dockerfile
# exo2
#   Dockerfile
#   app
#     exo2.py

# docker build -t exo2_image .
# docker run -it --rm  -v "$(pwd)/app:/home/app" exo2_image 

FROM python
# FROM python:3.12-slim
RUN pip install pandas
RUN pip install scikit-learn
RUN pip install joblib

WORKDIR /home/app
COPY    /app/exo2.py ./

CMD python exo2.py

