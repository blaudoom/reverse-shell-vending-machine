import socketserver

class customHttpServer(socketserver):

    def __init__(self, name):
        self.name = name

    def serve_forever(self):
        while self.must_server:
            self.handle_request()
