# Turkish Movie Search Engine

<br>

<p style="text-align:center">
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="200" > 
<img src="https://devnot.com/wp-content/uploads/2017/09/docker-compose.jpg" width="200" >

</p>
<br>
<br> 

Code contains a template for using FastAPI backend with BERT based similarity search.

Data source: [Turkish Movie Sentiment Analysis Dataset](https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset)
* I just selected unique movie names.

## Installation

There are only two prerequisites:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

<br>

``` bash
git clone https://github.com/silverstone1903/autocomplete-search-fastapi-bert.git
```

## Usage
### Start 

``` bash
docker-compose up -d
```

If you make any changes you can add `--build`. 

``` bash
docker-compose up --build -d
``` 

### Stopping containers

``` bash
docker-compose down
```
### Container Logs
When running containers with detached mode (`-d`) they work in the background thus you can't see the flowing logs. If you want to check compose logs with cli you can use `logs`.

``` bash
docker-compose logs --tail 50
```

* FastAPI (UI): http://localhost:8000


# Tests

If you want to run the tests inside the container;

```bash
docker-compose exec api pytest tests -sv
```