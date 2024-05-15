import socket
import tkinter as tk
from threading import Thread

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 6665))
    server.listen(5)

    while True:
        client, addr = server.accept()
        # create new thread to handle communication with the client
        thread = Thread(target=handle_client, args=(client, addr))
        # to execute the handle_client function concurrently
        thread.start()

def handle_client(client, addr):
    try:
        while True:
            request = client.recv(1024)
            if not request:
                break
            request = request.decode("UTF-8")
            message_listbox.insert(tk.END, f"From client {addr}: {request}")
            response_entry['state'] = 'normal'  # Enable response entry for input
            send_button['state'] = 'normal'  # Enable send button
            root_server.wait_variable(user_has_pressed_send)  # Wait for user to press send
            response_entry['state'] = 'disabled'  # Disable response entry after sending
            send_button['state'] = 'disabled'  # Disable send button after sending
            if server_response:
                try:  # Add try-except block for error handling
                    client.send(server_response.encode("UTF-8"))
                    message_listbox.insert(tk.END, f"Server: {server_response}")  # Display sent response
                except Exception as e:
                    print(f"Error sending response: {e}")
            else:
                print("No response entered by server operator.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

# GUI setup for server
root_server = tk.Tk()
root_server.title("Server Chat")

message_listbox = tk.Listbox(root_server, width=50, height=20)
message_listbox.pack(padx=10, pady=10)

server_response = ""  # Initialize server response variable

response_entry = tk.Entry(root_server, width=50)
response_entry.pack(padx=10, pady=5)
response_entry['state'] = 'disabled'  # Disable response entry initially

def send_response():
    global server_response
    server_response = response_entry.get()
    user_has_pressed_send.set(True)  # Signal that user has pressed send

send_button = tk.Button(root_server, text="Send", command=send_response)
send_button.pack(padx=10, pady=5)
send_button['state'] = 'disabled'  # Disable send button initially

user_has_pressed_send = tk.BooleanVar(root_server, value=False)  # Variable to track if user has pressed send

start_server_thread = Thread(target=start_server)
start_server_thread.daemon = True
start_server_thread.start()

root_server.mainloop()

