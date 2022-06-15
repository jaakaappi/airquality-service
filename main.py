from datetime import datetime, timedelta
from random import random

from flask import Flask, request, render_template, Response

app = Flask(__name__)

# _data = {
#     'temperature': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 10 + 20 for x in range(10)]
#     },
#     'humidity': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 20 + 10 for x in range(10)]
#     },
#     'co2': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 1100 + 400 for x in range(10)]
#     },
#     'tvoc': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 50 for x in range(10)]
#     },
#     'pm25': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 50 for x in range(10)]
#     },
#     'pm10': {
#         'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
#         'y': [random() * 25 for x in range(10)]
#     },
# }

_data = {
    'temperature': {
        'x': [],
        'y': []
    },
    'humidity': {
        'x': [],
        'y': []
    },
    'co2': {
        'x': [],
        'y': []
    },
    'tvoc': {
        'x': [],
        'y': []
    },
    'pm25': {
        'x': [],
        'y': []
    },
    'pm10': {
        'x': [],
        'y': []
    },
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/api", methods=['GET'])
def get_data():
    return _data


@app.route("/api", methods=['POST'])
def append_data():
    print(request.json)
    timestamp = datetime.now().isoformat()
    _data['temperature']['y'].append(request.json['temperature'])
    _data['temperature']['x'].append(timestamp)
    _data['humidity']['y'].append(request.json['humidity'])
    _data['humidity']['x'].append(timestamp)
    _data['co2']['y'].append(request.json['co2'])
    _data['co2']['x'].append(timestamp)
    _data['tvoc']['y'].append(request.json['tvoc'])
    _data['tvoc']['x'].append(timestamp)
    _data['pm25']['y'].append(request.json['pm25'])
    _data['pm25']['x'].append(timestamp)
    _data['pm10']['y'].append(request.json['pm10'])
    _data['pm10']['x'].append(timestamp)
    print(_data)
    return Response(status=200)

def main():
    app.run(host='localhost')


if __name__ == '__main__':
    main()
