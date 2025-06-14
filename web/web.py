from flask import Flask, send_from_directory, make_response

app = Flask(__name__, static_folder="", static_url_path="")


@app.route('/')
def index():
    response = make_response(send_from_directory('', 'index.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
    )
    return response


@app.route('/model/<path:path>')
def model_files(path):
    return send_from_directory('static/model', path)


def run_flask(port: int):
    app.run(port=port, debug=True, use_reloader=False)
