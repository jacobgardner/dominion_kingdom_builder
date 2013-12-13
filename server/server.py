import SocketServer


class DominionServer(SocketServer.StreamRequestHandler):
    def handle(self):
        self.command = self.rfile.readline().strip()
        print command

if __name__ == '__main__':
    server = SocketServer.TCPServer(('127.0.0.1', 1280), DominionServer)
    server.serve_forever()
