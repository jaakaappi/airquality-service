import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey

from flask import Flask, request, render_template, Response


def init_routes(app, cosmos_container):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/api", methods=['GET'])
    def get_data():
        query = 'SELECT TOP 60 c.co2, c.humidity, c.temperature, c.pm25, c.pm10, c.tvoc, c.timestamp FROM c ORDER BY c.timestamp'
        items = list(cosmos_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        print(items)
        return {'data': items}

    @app.route("/api", methods=['POST'])
    def append_data():
        print(request.json)
        timestamp = datetime.now().isoformat()
        _data = {
            'id': str(uuid.uuid4()),
            'timestamp': timestamp,
            **request.json
        }
        print(_data)

        cosmos_container.create_item(_data)

        return Response(status=200)

    return app


def init_cosmos(client):
    database_name = 'airquality-database'
    database = client.create_database_if_not_exists(id=database_name)

    container_name = 'airquality-container'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/timestamp"),
        offer_throughput=400
    )
    return container


def main():
    app = Flask(__name__)
    cosmos_client = CosmosClient('https://localhost:8081',
                                 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==')
    cosmos_container = init_cosmos(cosmos_client)
    app = init_routes(app, cosmos_container)
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
