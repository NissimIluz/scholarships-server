import asyncio

if __name__ == '__main__':
    from server import create_app
    app = create_app()
    app.run(debug=True, host='127.0.0.1', ssl_context='adhoc', use_reloader=True)  # Generate Adhoc Certs