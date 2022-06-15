from datetime import datetime, timedelta
from random import random

from flask import Flask, request, render_template

app = Flask(__name__)

_data = {
    'humidity': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 10 + 20 for x in range(10)]
    },
    'temperature': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 20 + 10 for x in range(10)]
    },
    'co2': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 1100 + 400 for x in range(10)]
    },
    'tvoc': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 50for x in range(10)]
    },
    'pm25': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 50 for x in range(10)]
    },
    'pm10': {
        'x': [(datetime.now() + timedelta(hours=x)).isoformat() for x in range(10)],
        'y': [random() * 25 for x in range(10)]
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
    _data['humidity'].append(request.json['humidity'])


def main():
    app.run(host='localhost')


if __name__ == '__main__':
    main()
