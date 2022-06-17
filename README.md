# airquality-service
Flask Python API and HTTP server for saving data and serving chart page for https://github.com/jaakaappi/airquality


## Running locally
Install Azure Functions Core Tools, Azure CLI, Python 3.9

Set env vars:
```
ENVIRONMENT=PRODUCTION
COSMOS_DB_URI=<get this from Azure>
COSMOS_DB_KEY=<get this from Azure>
```

```commandline
pip install requirements.txt
func start --python --port 5000
```

## Deployment
```commandline
az login
func azure functionapp publish airquality-function-app --python
```

## Monitoring

In Azure, function app > functions > logs > monitor

## Todo:
- axis tick scales
- button for time ranges / scrollable chart? https://www.chartjs.org/chartjs-plugin-zoom/latest/guide/options.html
- dark mode with settings saving
