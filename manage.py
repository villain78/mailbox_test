
from flask import g
from main import app
from common.utils import gen_uuid


@app.before_request
def before_request():
    g.request_id = gen_uuid()


def start_app():
    app.run(debug=True)


if __name__ == '__main__':
    start_app()
