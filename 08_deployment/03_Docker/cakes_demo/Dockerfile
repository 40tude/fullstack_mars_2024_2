# # De docker hub
# FROM python:3.9-alpine 
# COPY app.py /home/app/
# CMD python /home/app/app.py
# # CMD echo "Bonjour Pr FALKENexit


# FROM python:3.9-alpine 
# COPY app.py /home/app/
# WORKDIR /home/app
# RUN pip install numpy
# CMD python app.py


FROM python:3.9-alpine 
RUN pip install numpy

WORKDIR /home/app
#COPY app.py .

CMD python app.py

