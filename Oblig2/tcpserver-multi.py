from socket import *
import threading
import sys  # To terminate the program
import time

def now():
    """
    Returns the time of day
    """
    return time.ctime(time.time())

def handleClient(connectionSocket, addr):
    """
    A client handler function that processes the HTTP request
    """
    try:
        # Receive HTTP request from the client
        message = connectionSocket.recv(1024).decode()

        # Check if the message is empty (avoid "list index out of range")
        if not message:
            print(f"No message received from {addr}")
            connectionSocket.close()
            return

        # Extract the requested file from the HTTP request
        request_parts = message.split()
        if len(request_parts) < 2:
            print(f"Invalid HTTP request received from {addr}: {message}")
            connectionSocket.close()
            return

        filename = request_parts[1]

        # Default to "index.html" if the request is "/"
        if filename == "/":
            filename = "/index.html"

        try:
            # Open and read the file content
            with open(filename[1:], 'r') as f:
                outputdata = f.read()

            # Build the HTTP response header
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += f"Content-Length: {len(outputdata)}\r\n"
            response_header += "\r\n"  # End of headers

            # Send the response header and content to the client
            connectionSocket.sendall((response_header + outputdata).encode())

        except FileNotFoundError:
            # Send HTTP 404 Not Found response
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += "Content-Type: text/html\r\n\r\n"
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"

            # Send header and content just once
            connectionSocket.sendall((response_header + response_body).encode())

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        # Close the connection after handling the request
        connectionSocket.close()


def main():
    """
    Creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection joins.
    """
    serverPort = 8000  # Server port
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        serverSocket.bind(('', serverPort))
    except:
        print("Bind failed. Error : ")
        sys.exit()

    serverSocket.listen(5)  # Allow up to 5 pending connections
    print(f'The server is ready to receive at http://127.0.0.1:{serverPort}/')

    while True:
        # Wait for a connection from a client
        connectionSocket, addr = serverSocket.accept()
        print(f'Server connected by {addr} at {now()}')

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
        client_thread.start()

    serverSocket.close()

if __name__ == '__main__':
    main()
