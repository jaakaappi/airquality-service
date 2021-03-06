# airquality-service
Flask Python API and HTTP server for saving data and serving chart page for https://github.com/jaakaappi/airquality


## Running locally
Install Azure Functions Core Tools, Azure CLI, Python 3.9

Set env vars (prepend `set ` if on Windows):
```
ENVIRONMENT=PRODUCTION;
COSMOS_DB_URI=<get this from Azure>
COSMOS_DB_KEY=<get this from Azure>
```

```commandline
pip install requirements.txt
func start --python --port 5000
```

## Deployment
Set COSMOS_DB_URI and COSMOS_DB_KEY in app settings


```commandline
az login
func azure functionapp publish <function-app-name> --python
```

## Monitoring

```commandline
func azure functionapp logstream <function-app-name> --browser
```

## Todo:
- axis tick scales
- dark mode with settings saving
- fix graph timestamps to utc+3