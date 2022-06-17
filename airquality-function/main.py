import os
import uuid
from datetime import datetime
import logging

from azure.functions import HttpRequest, HttpResponse, Context, WsgiMiddleware
from azure.cosmos import CosmosClient, PartitionKey
from flask import Flask, request, render_template, Response
from pytz import timezone

logger = logging.getLogger('airquality')

def init_routes(app, cosmos_container):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/api", methods=['GET'])
    def get_data():
        # query = 'SELECT TOP 144 c.co2, c.humidity, c.temperature, c.pm25, c.pm10, c.tvoc, c.timestamp FROM c ORDER BY c.timestamp DESC'
        query = 'SELECT c.co2, c.humidity, c.temperature, c.pm25, c.pm10, c.tvoc, c.timestamp FROM c ORDER BY c.timestamp DESC'
        items = list(cosmos_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        request_charge = cosmos_container.client_connection.last_response_headers['x-ms-request-charge']
        print('Operation consumed {0} request units'.format(request_charge))

        json = {
            "temperature": {"x": [], "y": []},
            "humidity": {"x": [], "y": []},
            "co2": {"x": [], "y": []},
            "tvoc": {"x": [], "y": []},
            "pm25": {"x": [], "y": []},
            "pm10": {"x": [], "y": []},
        }
        for item in items:
            for key, value in item.items():
                if key != 'timestamp':
                    json[key]['y'].append(value)
                    json[key]['x'].append(item['timestamp'])

        return json

    @app.route("/api", methods=['POST'])
    def append_data():
        print(request.json)
        timestamp = timezone('Europe/Helsinki').localize(datetime.now()).isoformat()
        _data = {
            'id': str(uuid.uuid4()),
            'timestamp': timestamp,
            **request.json
        }

        cosmos_container.create_item(_data)
        request_charge = cosmos_container.client_connection.last_response_headers['x-ms-request-charge']
        print('Operation consumed {0} request units'.format(request_charge))

        return Response(status=200)

    return app


def init_cosmos(client):
    database_name = 'airquality-database'
    database = client.create_database_if_not_exists(id=database_name)

    container_name = 'airquality-container'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/timestamp")
    )
    return container

def init_logging():
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.debug('Logger ready')

def main(req: HttpRequest, context: Context)-> HttpResponse:
    app = Flask(__name__)
    if 'COSMOS_DB_URI' not in os.environ.keys() or 'COSMOS_DB_KEY' not in os.environ.keys():
        logging.error('Missing Cosmos DB env vars!')
        exit(1)
    cosmos_client = CosmosClient(os.environ['COSMOS_DB_URI'], os.environ['COSMOS_DB_KEY'])
    cosmos_container = init_cosmos(cosmos_client)
    app = init_routes(app, cosmos_container)
    # app.register_error_handler(400, lambda e: print(e))

    return WsgiMiddleware(app.wsgi_app).handle(req, context)
