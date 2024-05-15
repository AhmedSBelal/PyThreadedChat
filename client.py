import socket
import tkinter as tk
from threading import Thread

def send_message():
    message = message_entry.get()
    message_listbox.insert(tk.END, f"You: {message}")  # Print the sent message in the client's window
    response_label.config(text=f"Your message: {message}")
    client_thread = Thread(target=send_message_to_server, args=(message,))
    client_thread.start()
    message_entry.delete(0, tk.END)  # Clear the text field after sending the message

def send_message_to_server(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 6665))
    client.send(message.encode("UTF-8"))
    response = client.recv(1024).decode("UTF-8")
    message_listbox.insert(tk.END, f"Server response: {response}")
    # print(response)
    client.close()

# GUI setup for client
root_client = tk.Tk()
root_client.title("Client Chat")

message_listbox = tk.Listbox(root_client, width=50, height=20)
message_listbox.pack(padx=10, pady=10)

message_entry = tk.Entry(root_client, width=50)
message_entry.pack(padx=10, pady=5)

send_button = tk.Button(root_client, text="Send Message", command=send_message)
send_button.pack(padx=10, pady=5)

response_label = tk.Label(root_client, text="")
response_label.pack(padx=10, pady=5)

root_client.mainloop()
