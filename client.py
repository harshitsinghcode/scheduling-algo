import socket
import json

class IOSchedulingClient:
    def __init__(self, host='localhost', port=65432):
        """
        Initialize the I/O Scheduling Client
        :param host: Server host address
        :param port: Server port number
        """
        self.host = host
        self.port = port

    def connect(self):
        """
        Connect to the I/O Scheduling Server
        """
        try:
            # Create socket for each connection attempt
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            # Receive scheduling data from server
            data = client_socket.recv(4096).decode('utf-8')
            scheduling_data = json.loads(data)
            # Print received scheduling information
            print("=== Client Received Scheduling Information ===")
            print("Client ID:", scheduling_data['client_id'])
            print("\nProcess Priorities:", scheduling_data['process_priorities'])
            print("I/O Request Times:", scheduling_data['io_request_times'])
            print("\n--- Payoff Matrix ---")
            for row in scheduling_data['payoff_matrix']:
                print(row)
            print("\n--- Nash Equilibrium Strategies ---")
            for process, device in scheduling_data['nash_equilibrium']:
                print(f"Process {process}: Optimal Device {device}")
            print("\n--- Optimal Device Allocation ---")
            for device, processes in scheduling_data['optimal_allocation'].items():
                print(f"Device {device}: Processes {processes}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    client = IOSchedulingClient()
    client.connect()
