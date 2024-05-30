# A partir du répertoire exo3 où se trouve Dockerfile
# docker build -t exo3_image .
# docker run -it --rm -v "$(pwd)/app:/home/app"  -p 1024:5000 exo3_image
# Brancher sont client Web sur : localhost:1024

# Arborescence des fichiers
# exo3
#   Dockerfile
#   requirements.txt
#   app
#     exo3.py

# Le fichier requirements.txt contient les 4 lignes suivantes
# streamlit
# pandas
# plotly
# numpy


FROM python:3.12-slim

RUN     --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip install --requirement /tmp/requirements.txt

# inform Docker that the container listens on the specified network ports at runtime
# on peut le garder ou le virer - j'ai toujours pas compris 
# On s'en fiche en fait c'est mata data : https://spacelift.io/blog/docker-expose-port
# EXPOSE 5000

WORKDIR /home/app
COPY    /app/exo3.py ./

ENTRYPOINT ["streamlit", "run", "exo3.py", "--server.port=5000", "--server.address=0.0.0.0"]

