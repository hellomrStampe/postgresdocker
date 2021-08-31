# Postgres on Docker
> it's time for your local CSVs, Excel files and DataFrames to live in Postgres 

![](cover.png)
I just wanted to spin up Postgres DB to push and pull my tabular data with a single command.
This is repo is the outcome of my laziness.

### Setup:
```bash
git clone https://github.com/Proteusiq/postgresocker
docker volume create --name pgdatax
```
We are going to store our data in pgdatax volume that will outlive docker containers creations and destructions.
To make sure we do not have issues with different Postgres version, you can pin a version down in `containers/postgres/Dockerfile`

### Running services:
Navigate to project directory where `docker-compose.yml` file is and execute:
```bash
docker-compose up -d
```
### Ending services
Navigate to project directory where `docker-compose.yml` file is and execute:
```bash
docker-compose down
```

### INFO:
<b>pgAdmin UI</b> is at localhost:5050 with login: `jamesbond@007.com` | password: `goldeneye` <br>

Create connection to Postgres <br>
New Server > General: name `any_name` > Connection: hostname `postgres`,  username: `jamesbond`, password: `goldeneye` 

## Test Example
To run the test example
```bash
# tip: works best if you create environment
python -m pip install -r requirements
python example.py
```
