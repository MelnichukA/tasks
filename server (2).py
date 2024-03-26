import socket
import threading

HOST = "127.0.0.1"
# PORT = 21042
PORT = 9090
LISTENER_LIMIT = 2
active_clients = []
BUFFER_SIZE = 2048
message_dict = {}


def listen_for_messages(client: object, username: str):

    while 1:
        message = client.recv(BUFFER_SIZE).decode('utf-8')
        if message != '':

            message_history(message, username, client)

            final_msg = f'{username}~{message}'
            send_messages_to_all(final_msg)




def message_history(message: str, username: str, client: object):
    if username in message_dict:
        if isinstance(message_dict[username], list):
            message_dict[username].append(message)
        else:
            print('not fck list')
    else:
        print('not username')

    writing_message(message_dict)

    # username, content = message.split('~')
    if message == "ls":
        file_path = "messages_hist.txt"

        try:
            with open(file_path, "r") as file:
                # Читаємо кожний рядок з файлу та додаємо його до списку
                my_list = [send_messages_to_all(line.strip()) for line in file.readlines()]

            print("Всі повідомлення:", my_list)
        except Exception as e:
            print("Сталася помилка при зчитуванні з файлу:", e)

        # for message in message_list:
        #     data = f'{username}~{message}'
        #     print(data)
        #     send_messages_to_all(data)


def writing_message(message_list):
    file_path = "messages_hist.txt"  # Шлях до файлу, куди ви хочете записати список
    try:
        with open(file_path, "w") as file:
            # Запис кожного ключа та його значення у файл
            for key, value in message_dict.items():
                # Якщо значення є списком, конвертуємо його до рядка
                if isinstance(value, list):
                    value_str = ", ".join(value)
                else:
                    value_str = str(value)
                file.write("%s: %s\n" % (key, value_str))

    except Exception as e:
        print("Сталася помилка при записі у файл:", e)

    # # Зчитуємо існуючий файл зі словником
    # existing_dict = OrderedDict()
    # try:
    #     with open(existing_file_path, "r") as file:
    #         for line in file:
    #             key, value = line.strip().split(": ")
    #             if key in existing_dict:
    #                 existing_dict[key].append(value)
    #             else:
    #                 existing_dict[key] = [value]
    # except FileNotFoundError:
    #     print("Файл із словником не знайдено. Створюємо новий файл.")
    #
    # # Оновлення словника з новими значеннями
    # messages_dict = {}
    #
    # for key, value in messages_dict.items():
    #     if key in messages_dict:
    #         message_dict[key].append(value)
    #     else:
    #         existing_dict[key] = [value]
    #
    # # Запис оновленого словника у файл
    # try:
    #     with open(existing_file_path, "w") as file:
    #         for key, values in existing_dict.items():
    #             for value in values:
    #                 file.write("%s: %s\n" % (key, value))
    #     print("Словник був успішно оновлений та записаний у файл", existing_file_path)
    # except Exception as e:
    #     print("Сталася помилка при записі у файл:", e)


# def add_value_to_dict(dictionary, key, value):
#     if key in dictionary:
#         if isinstance(dictionary[key], list):
#             dictionary[key].append(value)
#         else:
#             dictionary[key] = [dictionary[key], value]
#     else:
#         dictionary[key] = [value]


def send_message_to_client(client: object, message: str):

    client.sendall(message.encode())


def send_messages_to_all(message: str):
    
    for user in active_clients:
        send_message_to_client(user[1], message)
        # who is it? what is user[1]? ( specify type )


def client_handler(client: object):

    while 1:
        username = client.recv(BUFFER_SIZE).decode("utf-8")
        if username != '':
            active_clients.append((username, client))
            message_dict[username] = []
            print(message_dict)
            break
        else:
            print("Client username is empty. Try again.")
    print(active_clients)

    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Error: {e}")  # what type of Exception? It's better to avoid stubs that catch any exceptions
        print(f"Unable to bind to host: {HOST} and port: {PORT}")
    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0], address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()