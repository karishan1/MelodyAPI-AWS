# MelodyAPI

MelodyAPI is a music analysis API that classifies genre, mood/theme and instrumentation of audio filesz.

Executable was not provided because MelodyAPI depends on a local instance of DynamoDB and deployed on AWS
To run MelodyAPI locally: 

# CLONE THE REPO
git clone https://github.com/karishan1/MelodyAPI-AWS.git
cd MelodyAPI-AWS

# CREATE CONDA ENVIRONMENT WITH PYTHON 3.11
conda create -n melodyapi python=3.11
conda activate melodyapi

# INSTALL DEPENDENCIES
pip install -r requirements.txt

# RUN FASTAPI SERVER
uvicorn app.main:app --reload --port 8000

# START DYNAMODB LOCAL ON A NEW TERMINAL (INSTALL IF YOU HAVEN'T)
cd dynamodb_local/
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

# ACCESS DOCS PAGE
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc