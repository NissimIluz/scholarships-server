import asyncio


def run_serve():
    from waitress import serve
    serve(get_server_app(), host="0.0.0.0", port=8080)


def run_serve_in_localhost():
    from waitress import serve
    serve(get_server_app(), listen="127.0.0.1:5000", url_scheme='https')


def get_server_app():
    from server import create_app
    app = create_app()
    return app


if __name__ == '__main__':
    run_serve()
