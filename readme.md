# Dataset Analyzer and Preprocessor

## Features

### Changelog
- Added more metrics as goal metrics
- Added images datasets
- Add method for reducing dataset (balanced vs uniform)
- Added notebook containing analysis of the tool on actual data
- Uploaded to github and dockerized 

### To do

- [ ] Add more TS datasets
- [ ] Clean UI
- [ ] Add a section that shows user what are the environmental impacts when using the tool (carbon emission reduction, etc)



## Run the tool

### Docker and Docker-Compose (Recommended)


- Install [Docker](https://www.docker.com/)
- From the root of the project run the following


First install everything with
```bash
docker-compose --build
```

Now to run
```bash
docker-compose up -d
```

The first time the database needs to be set, run in order the following commands

```bash
curl -X 'GET' 'http://localhost:5000/api/load_experiments_on_db?reset_db=true' -H 'accept: application/json'

curl -X 'GET' 'http://localhost:5000/api/load_completeness_curves?load_only_missing=false' -H 'accept: application/json'

curl -X 'GET' 'http://localhost:5000/api/train_regressors' -H 'accept: application/json'
```

You can now visit the interface in https://localhost:8080

To finish the process after
```bash
docker-compose down
```

### Installing everything manually


- Install the following requirements
  - For the backend
    - python 3.10
    - From the `backend/` directory, run `pip install -r requirements.txt`
  - For the frontend
    - install `node 16`
    - From the 'frontend/' directory, run `npm install` and `npm run build`

Now to run the backend
```bash
uvicorn main:app --port 3000 
```
And the frontend
```bash
npm run serve
```

The first time the database needs to be set, run in order the following commands

```bash
curl -X 'GET' 'http://localhost:5000/api/load_experiments_on_db?reset_db=true' -H 'accept: application/json'

curl -X 'GET' 'http://localhost:5000/api/load_completeness_curves?load_only_missing=false' -H 'accept: application/json'

curl -X 'GET' 'http://localhost:5000/api/train_regressors' -H 'accept: application/json'
```

You can now visit the interface in https://localhost:8080