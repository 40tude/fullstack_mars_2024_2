# A partir du répertoire exo1 où se trouve Dockerfile
# exo1
#   Dockerfile
#   app
#     exo1.py

# docker build -t exo1_image .

FROM python:3.9-alpine 
RUN pip install numpy

WORKDIR /home/app
COPY    /app/exo1.py ./

CMD python exo1.py

