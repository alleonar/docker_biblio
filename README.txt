# 1_CONSTRUIRE L'IMAGE DOCKER
(dans le répertoire contenant le dockerfile)
docker build -t bibliodrive.

# 2_DEMARRER LE CONTENEUR
(avec POWERSHELL)
Dev ( écrase le COPY . . et ne prends pas en compte le .dockerignore / avec terminal open pour ne pas lancer de server):
docker run -it -v ${PWD}:/usr/src/app -p 8000:8000 bibliodrive bash

Prod avec COPY . . dans le dockerfile et le .dockerignore complété:
docker run --name bibliodrive_prod -p 8000:8000 -d bibliodrive:latest


# Memo:

RUN: exécuté au build

CMD: exécuté au docker run ou compose