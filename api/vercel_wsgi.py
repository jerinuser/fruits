def handle_request(app, environ, start_response):
    return app(environ, start_response)