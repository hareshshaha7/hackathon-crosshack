# Hackathon - Crosshack
-------

<b> Prerequisite </b>

Python version: `3.9`

-------

<b> Local Setup </b>

- Install python 

```commandline
pyenv install 3.9
pyenv local 3.9
```

- Create local virtual environment

```commandline
python -m venv hackathon 
source hackathon/bin/activate
```

- Install required packages

```commandline
pip install --upgrade pip
pip install -r requirements.txt
```
-------

<b> Run the Project </b>

- Add valid values in  `.env` file.
- Run plain python application
```commandline
python resend_errors.py
```

- Run flask server to test rest endpoints
```commandline
flask --app=main.py run
```
-------

<b> Install vector database: Milvus </b>

```commandline
wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose.yml -O docker-compose.yml\n
sudo docker-compose up -d\n
docker-compose up -d\n
docker compose ps
docker port milvus-standalone 19530/tcp
```
-------

<b> Example </b>

- Test API
```commandline
curl --location 'http://127.0.0.1:5000/'
```

- Get answer for your question 
```commandline
curl --location 'http://127.0.0.1:5000/answer' \
--header 'Content-Type: application/json' \
--data '{
    "query": "What is the main point of the transcript?"
}'
```
