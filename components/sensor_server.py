import socket
import json
import time
from data_generator import generator

HOST = '0.0.0.0'
PORT = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = s.accept()
print("Connected by", addr)

gen = generator(target_hz=200)

try:
    while True:
        imu_data, lc_data = next(gen)
        msg = {"imu": imu_data, "load_cell": lc_data}
        conn.sendall((json.dumps(msg) + "\n").encode("utf-8"))
        time.sleep(0.001)
except KeyboardInterrupt:
    print("Shutting down server")
    conn.close()
    s.close()