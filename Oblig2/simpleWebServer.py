from socket import *
import sys  # To terminate the program

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Define the port number
serverPort = 8000  # Change to the desired port

# Bind the server to IP and port
serverSocket.bind(('', serverPort))

# Start listening for client connections
serverSocket.listen(1)

print(f"Server is running at http://127.0.0.1:{serverPort}/")

while True:
    # Wait for a connection from a client
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive HTTP request from the client
        message = connectionSocket.recv(1024).decode()

        # Check if the message is empty (avoid "list index out of range")
        if not message:
            connectionSocket.close()
            continue

        # Extract the requested file from the HTTP request
        request_parts = message.split()
        if len(request_parts) < 2:
            print("Invalid HTTP request received:", message)
            connectionSocket.close()
            continue

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

            # Send the response header and content to the client using sendall()
            connectionSocket.sendall(response_header.encode() + outputdata.encode())

        except FileNotFoundError:
            # Send HTTP 404 Not Found response
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += "Content-Type: text/html\r\n\r\n"
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"

            # Send the response header and content to the client
            connectionSocket.sendall(response_header.encode() + response_body.encode())

        # Close the connection
        connectionSocket.close()

    except Exception as e:
        print(f"Error: {e}")
        connectionSocket.close()

# Close the server (this code is never reached due to while True loop)
serverSocket.close()
sys.exit()
