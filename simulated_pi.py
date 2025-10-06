import socket
import threading
import time

class SimulatedPiConnectionOnly:
    def __init__(self, host="127.0.0.1", port=5050):
        self.host = host
        self.port = port
        self.running = False
        self.server_sock = None

    def start(self):
        self.running = True
        threading.Thread(target=self._run_server, daemon=True).start()
        print(f"[SimulatedPi] Listening on {self.host}:{self.port}")

    def _run_server(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)

        while self.running:
            try:
                client_sock, addr = self.server_sock.accept()
                print(f"[SimulatedPi] Client connected from {addr}")
                threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True).start()
            except OSError:
                break

    def _handle_client(self, client_sock):
        try:
            # Receive SUBSCRIBE (optional)
            client_sock.recv(1024)
            # Keep connection alive without sending data
            while self.running:
                time.sleep(0.1)
        except:
            pass
        finally:
            client_sock.close()

    def stop(self):
        self.running = False
        if self.server_sock:
            self.server_sock.close()
        print("[SimulatedPi] Server stopped")


if __name__ == "__main__":
    server = SimulatedPiConnectionOnly()
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
