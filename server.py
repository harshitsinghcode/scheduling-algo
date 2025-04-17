import socket
import threading
import json
import uuid
import numpy as np
from scheduler import IODeviceScheduler

class IOSchedulingServer:
    def __init__(self, host='0.0.0.0', port=65432):
        """
        Initialize the I/O Scheduling Server
        :param host: Server host address
        :param port: Server port number
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        # Device scheduler
        self.scheduler = IODeviceScheduler()
        # Connected clients
        self.clients = {}

    def handle_client(self, client_socket, client_address):
        """
        Handle individual client connections
        :param client_socket: Socket connection to client
        :param client_address: Client address information
        """
        try:
            # Generate unique client ID
            client_id = str(uuid.uuid4())
            self.clients[client_id] = client_socket
            # Send initial scheduling information
            initial_data = {
                'client_id': client_id,
                'process_priorities': self.scheduler.process_priorities,
                'io_request_times': self.scheduler.io_request_times,
                'payoff_matrix': self.scheduler.payoff_matrix.tolist(),
                'nash_equilibrium': [(int(p), int(d)) for p, d in self.scheduler.nash_equilibrium],
                'optimal_allocation': {int(k): [int(v) for v in vs] for k, vs in self.scheduler.optimal_allocation.items()}
            }
            # Send data to client
            client_socket.send(json.dumps(initial_data).encode('utf-8'))
            # Keep connection open for potential further interactions
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                # Process client requests if needed
                print(f"Received from {client_address}: {data}")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            if client_id in self.clients:
                del self.clients[client_id]

    def start(self):
        """
        Start the server and listen for client connections
        """
        print(f"Server started on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
        except Exception as e:
            print(f"Error in server: {e}")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = IOSchedulingServer()
    server.start()