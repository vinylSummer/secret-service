# Goofy Meme Service
Provides CRUD operations for Memes(image_data + optional caption)

![](docs/technical_assignment.png)

## Design
The service consists of 4 microservices:
1) Meme Service - uses other microservices to do the required operations
2) Image Service - manages images, not necessarily memes
3) Database Service - contains meme metadata, like caption and image_id
4) Storage Service - stores data, not necessarily memes or images

Each microservice is located in its dedicated folder inside this monorepo.
No microservice requires code from others, so they could've potentially been separated into different repos

Microservices intercommunication is achieved via sync REST API.
Memes are sent in json format, meme image data is sent in base 64 representation.
Message queues could've been used for the communication, but I chose the prior option for the sake of simpler design

Database service uses Postgres database that gets set up programmatically via docker compose.
Migrations are applied via docker-entrypoint-initdb.d

Storage service uses MinIO as an S3 compatible data store.
It isn't deployed programmatically nor is expected to be deployed manually,
instead play.min.io will be used.
Bucket name should be specified as an env variable and can't be changed without a restart


## Usage
Clone this repo to your local machine:
```shell
git clone https://gitlab.com/vinyl_summer/goofy-meme-service.git && cd goofy-meme-service
```
### 1. Set up environment variables.
(For development purposes you can use .env file, see .env.example for each microservice)

#### Meme Service
DB_SERVICE_ENDPOINT - required, default - http://db-service:8081/memes

IMAGE_SERVICE_ENDPOINT - required, default - http://image-service:8082/images

HTTP_HOST - optional, default - 0.0.0.0

HTTP_PORT - optional, default - 8080

LOG_LEVEL - optional, default - INFO

#### Image Service
S3_ENDPOINT - required, default - http://s3-service:8083/data

HTTP_HOST - optional, default - 0.0.0.0

HTTP_PORT - optional, default - 8082

LOG_LEVEL - optional, default - INFO

#### Database Service
DB_URL - required, default - postgresql://test_user:test_password@postgres-db:5432/testDB?sslmode=disable

HTTP_HOST - optional, default - 0.0.0.0

HTTP_PORT - optional, default - 8081

LOG_LEVEL - optional, default - INFO

#### Storage Service
S3_ENDPOINT - required, default - play.min.io

S3_ACCESS_KEY - required, default - NONE!

S3_SECRET_KEY - required, default - NONE!

S3_BUCKET - optional, default - test-bucket

HTTP_HOST - optional, default - 0.0.0.0

HTTP_PORT - optional, default - 8083

LOG_LEVEL - optional, default - INFO


**Important!!!**

You must get your own S3_ACCESS_KEY and S3_SECRET_KEY for the storage service.

The instructions for that are located [here](https://min.io/docs/minio/linux/administration/minio-console.html#minio-console-play-login)

### 2. Start the services
```shell
docker-compose up -d
```

### 3. Enjoy!
Here is the endpoint summary, assuming you didn't change the defaults:
1) Meme Service: http://127.0.0.1:8080/memes 
Swagger docs: http://127.0.0.1:8080/docs
2) Image Service: http://127.0.0.1:8082/images
Swagger docs: http://127.0.0.1:8082/docs
3) Database Service: http://127.0.0.1:8081/memes
Swagger docs: http://127.0.0.1:8081/docs
4) Storage Service: http://127.0.0.1:8083/data
Swagger docs: http://127.0.0.1:8083/docs

## Tests
There are unit tests for each microservice in their respective tests folder. Here's how to run them:

#### 1. Cd into the folder for the microservice you want to run the tests for
```shell
cd meme_service
```

#### 2. Create python venv and activate it
```shell
python -m venv ./venv
```
```shell
source ./venv/bin/activate
```

#### 3. Install dev requirements
```shell
pip install -r requirements_dev.txt
```

#### 4. Run the tests
```shell
python -m pytest -v -s tests
```
