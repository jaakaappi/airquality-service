from flask import Flask, request, render_template

app = Flask(__name__)

_data = {
    'humidity': [1, 2, 3, 4, 5, 6]
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
