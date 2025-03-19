import argparse
import socket

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Simple HTTP Client")
    parser.add_argument("-i", "--ip", required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port number")
    parser.add_argument("-f", "--file", required=True, help="Filename to request from the server")

    args = parser.parse_args()

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((args.ip, args.port))

        # Format the HTTP GET request
        request = f"GET /{args.file} HTTP/1.1\r\nHost: {args.ip}\r\n\r\n"

        # Send the request
        client_socket.send(request.encode())

        # Receive the response in chunks
        response = ""
        while True:
            chunk = client_socket.recv(4096).decode()
            response += chunk
            if len(chunk) < 4096:  # No more data left
                break

        print("Server Response:\n")

        # Optionally, print the file content to the terminal
        if "HTTP/1.1 200 OK" in response:
            # Extract content after the headers and print it
            content_start = response.find("\r\n\r\n") + 4
            print(response[content_start:])
        else:
            print(response)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    main()
