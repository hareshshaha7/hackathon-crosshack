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

- Run flask server to test rest endpoints
```commandline
flask --app=main.py run
```
-------

<b> Install vector database: Milvus </b>

- To install `docker-compose`
```commandline
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
```

```commandline
wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose.yml -O docker-compose.yml

sudo docker-compose up -d

docker-compose up -d

docker compose ps

docker port milvus-standalone 19530/tcp
```
-------

<b> Example </b>

- Test API
```commandline
curl --location 'http://127.0.0.1:5000/'
```

- API to load data
```commandline
curl --location 'http://127.0.0.1:5000/load_data' \
--form 'file=@"/Users/haresh/Downloads/DataSource.docx"'
```

- API to get answer for your question 
```commandline
curl --location 'http://127.0.0.1:5000/get_reply' \
--header 'Content-Type: application/json' \
--data '{
    "query": "What is the main point of the transcript?"
}'
```
