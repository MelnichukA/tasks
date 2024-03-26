import socket

def server():
    try:
        host = socket.gethostname()
        port = 21042
        s = socket.socket()
        s.bind((host, port))
        s.listen(2)
        c, address = s.accept()
        print(f"Connected to: {address}")
        DATA = []
        while True:
            data = c.recv(1024).decode()
            DATA.append(data)
            if not data:
                break
            print(f"Received from client: {data}")

            response = input("Enter response to send to client: ")
            c.send(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c.close()


if __name__ == "__main__":
    server()