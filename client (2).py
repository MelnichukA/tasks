import socket
import threading

HOST = "127.0.0.1"
# PORT = 21042
PORT = 9090
BUFFER_SIZE = 2048


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(BUFFER_SIZE).decode("utf-8")

        if message.lower().split('~')[1] != "off":
            username, content = message.split('~')
                        # username = message.split("~")[0]  # why you split message twice? (username, content = message.split('~'))
                        # content = message.split("~")[1]
            print(f"[{username}] {content}")
        else:
            print("Message received from client for stop program")
            exit()


def send_message_to_server(client):
    message = ""
    print("Type 'off' to exit. 'ls' to get all messages")

    while message.lower().split() != "off":

        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Message is empty")
            continue

    exit()


def communicate_to_server(client):
    username = input("Enter username: ")

    while len(username) == 0:
        print("Username cannot be empty. Try again. ")
        username = input("Enter username: ")

    client.sendall(username.encode())

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client)





def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")


    except Exception as e:
        print(f"Error: {e}")
        print(f"Unlable to connect to server {HOST}, {PORT}")
    communicate_to_server(client)


if __name__ == "__main__":
    main()

