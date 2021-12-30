import cv2
import threading
import socket
import pickle
import struct
from scapy.all import *
import time
from PIL import Image
from PIL import ImageTk


## @package lancamera
#  This package exposes the finctionalities of the cameras
#  available in the LAN.
#


## \brief Class LanCamera
#
#  Main class of the package lancamera, with functionalities to list camera servers and their cameras.
class LanCamera:

    def __init__(self, HOST='127.0.0.1', PORT=9000):
    
        self.__running = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## \brief List servers listening to a given port.
    #
    #  List all available servers on LAN that have certain ports open.
    #  The opened ports should belong to the interval 'port_range'.
    def list_servers(self, port_range: list):

        hosts = self.__scan_ports(port_range)
        if len(hosts) > 0:
            print("Servidores encontrados: ")
            for host, ports in hosts.items():
                print(f"IP Servidor: {host}; Portas abertas: {ports}")
        else:
            print("Nenhum servidor foi encontrado")

        return hosts

    ## \brief List open ports of the hosts in the LAN.
    #
    # For each ip obtained through __get_ips(), determines which port, in 'port_range' is open.
    def __scan_ports(self, port_range: list):

        if type(port_range) is int:
            start = port_range
            end = start+1
        else:
            start = port_range[0]
            end  = port_range[1]

        ips = self.__get_ips()
        ips.append("127.0.0.1")
        hosts = {}
        for ip in ips:
            ports = []
            print(f"Scaneando portas {start}-{end-1} do host {ip}")
            for port in range(start, end):
                if self.__scan_port(ip, port):
                    ports.append(port)

            if len(ports) > 0:
                hosts[ip] = ports

        return hosts

    ## \brief Tries to connect to a port of an IP address.
    #
    #  Tries to connect to a specific port and IP to see if the port is open
    def __scan_port(self, ip, port, timeout=2):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        if s.connect_ex((ip, port)) == 0:
            s.sendall(b'END')
            s.close()
            return True

        s.close()
        return False

    ## \brief Get all hosts in the LAN.
    #
    #  Pings via ARP protocol all hosts in the network to obtain the IPs of available hosts in the network
    #  (MUST RUN AS ROOT TO PING VIA ARP)
    def __get_ips(self, network='192.168.1.0/24'):

        ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network),timeout=2)
        ips = []
        for res in ans.res:
            ips.append(res.answer.psrc)

        return ips

    ## \brief List all cameras in localhost.
    #
    #  List all the available capture devices with index up to 'num' in localhost .
    def list_cams_local(self, num):

        index = 0
        v = []
        i = num
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                v.append(index)
                cap.release()
                
            index += 1
            i -= 1
        return v


## \brief Class Client
#
#  Class with functionalities to query and connect to camera servers.
class Client(LanCamera):

    def __init__(self, HOST='127.0.0.1', PORT=9000):

        self.__running = False
        self.__streaming = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_commands = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = b''

    def set_host(self, host, port):
        self.__host = host
        self.__port = port


    def list_cams_at(self, ip, port_range):
        if len(port_range) > 1:
            start = port_range[0]
            end = port_range[1]

        else:
            start = end = port_range

        devices = []
        for port in range(start, end):
            if self.__scan_port(ip, port):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    s.sendall(b"LIST")
                    cams = s.recv(1024).decode()
                    cams = cams.replace('[','')
                    cams = cams.replace(']','')
                    cams = cams.split(',')
                    devices.append(cams)
                    print(f'Cameras do servidor {ip}:{port} -> {cams}')
                    s.sendall(b"END")

        return devices
    ## \brief List cameras from available hosts in the network.
    #
    #  List all cameras and hosts with available cameras in the LAN.
    def list_cams_lan(self):

        hosts = self.list_servers(9001)
        devices = {}
        for ip, ports in hosts.items():
            for port in ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    s.sendall(b"LIST")

                    cams = s.recv(1024).decode()
                    cams = cams.replace('[','')
                    cams = cams.replace(']','')
                    cams = cams.split(',')
                    devices[ip] = cams
                    print(f'Cameras do servidor {ip}:{port} -> {cams}')
                    s.sendall(b"END")

        return devices

    ## \brief Connects to a streaming server.
    #
    #  Starts a thread that does the connection with the streaming server
    #  If record=True, __handle_conn will save the frames to the hard drive
    def start_connection(self, record=False, container=None):

        if self.__streaming: 
            print("O cliente já está rodando")
        else:
            self.__socket.connect((self.__host, self.__port))
            self.__streaming = True
            # self.__socket_commands.connect((self.__host, self.__port+1))
            # server_thread = threading.Thread(target=self.__connect, args=(record, container, ))
            # server_thread.start()

    def start_commands_connection(self):

        if self.__running:
            print("O cliente já está conectado")
        else:
            self.__running = True
            self.__socket_commands.connect((self.__host, self.__port+1))

    ## \brief Connects to a streaming server.
    #
    #  Connects to the streaming server and starts a thread the handles the streaming data that is received
    #  If record=True, __handle_conn will save the frames to the hard drive
    def __connect(self, record, container):

        if self.__streaming:
            print("O cliente já está conectado")

        else:
            self.__streaming = True
            self.__socket.connect((self.__host, self.__port))

    ## \brief Sends a command to the server.
    #
    #  Sends the specified command to the server
    def send_command(self, command):

        msg_len = struct.pack('i', len(command))
        self.__socket_commands.sendall(msg_len + command.encode())

    def recv_response(self):
        return self.__socket_commands.recv(1024)

    ## \brief Receives frame from the server.
    #
    #  Receives, decodes and displays a single streaming frame that was received from the server
    #  This method is designed to be accessed by the GUI interface in order to display
    #  the frame on the application window
    def recv_frame(self, img_data_size):

        quit = False

        while len(self.data) < img_data_size:
            recv = self.__socket.recv(4096)
            self.data += recv

            if self.data == b'':
                self.__socket.close()
                quit = True
                break

        if quit:
            return None

        msg_size = self.data[:img_data_size]
        self.data = self.data[img_data_size:]

        msg_size = struct.unpack(">L", msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.__socket.recv(4096)
            if self.data == b'':
                self.stop_client()
                quit = True
                break
        if quit:
            return None
            
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]  
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        return frame

    ## \brief Stop connection.
    #
    #  Stop the client connection to the streaming server
    def stop_commands_client(self):

        if self.__running:
            self.__running = False
            self.__socket_commands.close()

        else:
            print("Não tem clientes rodando")

    def stop_streaming_client(self):

        if self.__streaming:
            self.__streaming = False
            self.__socket.close()

        else:
            print("Não tem clientes rodando")

## \brief Class Server.
#
#  Class with functionalities to share the camera and stream video.
class Server(LanCamera):

    def __init__(self, HOST='127.0.0.1', PORT=9000, device=0):
    
        self.__running = False
        self.__streaming = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_commands = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__cam = None
        self.connections = []
        self.__init_socket()

    ## \brief Initialize socket
    #
    #  Initializes all sockets binding them to specific ports
    def __init_socket(self):
        self.__socket.bind((self.__host, self.__port))
        self.__socket_commands.bind((self.__host, self.__port+1))

    ## \brief Initialize camera
    #
    #  Initializes video capture device
    def __init_camera(self, device):
        self.__cam = cv2.VideoCapture(device)

    ## \brief Destroy camera
    #
    #  Destroy video capture device and window data structures
    def __cleanup(self):
        self.__cam.release()
        cv2.destroyAllWindows()

    def list_cams_local(self, num):

        index = 0
        v = []
        i = num
        while i > 0:

            cap = cv2.VideoCapture(index)

            if cap.isOpened():
                v.append(index)
                cap.release()
                
            index += 1
            i -= 1
        return v

    ## \brief Start command server thread
    #
    #  Start a thread to receive commands from the client
    def start_commands_server(self, routine_handler=None):

        if self.__running:
            print("O servidor já está rodando")

        else:
            thread = threading.Thread(target=self.__server_listen_commands, args=(routine_handler, ))
            thread.start()

    ## \brief Listen to port.
    #
    #  Accept connections coming to the port that handles commands and start a thread to
    #  handle incoming commands
    def __server_listen_commands(self, routine_handler=None):

        self.__running = True

        while self.__running:
            self.__socket_commands.listen()
            conn, addr = self.__socket_commands.accept()
            thread = threading.Thread(target=self.__handle_commands, args=(conn, routine_handler, ))
            thread.start()

    ## \brief Handle received commands.
    #
    #  Handle the data received, which should be a command specifying an action.
    #  A function that treats the command should be specified as an argument (routine_handler)
    #  in order to respond the received command properly.
    def __handle_commands(self, conn, routine_handler):

        while self.__running:

            try:
                data = conn.recv(1024)
            except:
                conn.close()
                break

            if data == b"LIST":

                cams = self.list_cams_local(5)
                conn.sendall(str(cams).encode())

            if b'ROUTINE' in data:

                while True:
                    size = struct.unpack('i', conn.recv(struct.calcsize ('i')))[0]
                    data = ''
                    msg = conn.recv(size)
                    data += msg.decode()
                    data = data.replace("\"", "")

                    if data == 'ROUTINEEND':
                        print(data)
                        break

                    print(data)
                    cmd, instruction = data.split(';')
                    # data = conn.recv(1024)

                    routine_handler(cmd, instruction)   

            if b'SELECT' in data:
                device = int(data.split(b' ')[1])
                print(device)
                self.__init_camera(device)

                while not self.__cam:
                    time.sleep(0.1)

            if data == b'END':
                conn.close()
                break

    ## \brief Stop command server thread
    #
    #  Stop the server that is waiting for connections to execute commands
    def stop_commands_server(self):

        if self.__running:
            self.__running = False

            closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closer.connect((self.__host, self.__port+1))
            closer.close()
            self.__socket_commands.close()

        else:
            print("O servidor não está realizando o streaming")
  
    ## \brief Start video streaming thread.
    #
    #  Starts a thread to listen for connections for video streaming
    def start_stream_server(self, device):

        if self.__streaming:
            print("O servidor já está realizando o streaming")

        else:
            # self.__init_camera(0) # this is temp
            server_thread = threading.Thread(target=self.__server_listen, args=(device, ))
            server_thread.start()

    ## \brief Listen to streaming requisitions.
    #
    #  Listens for an incoming connection and starts a thread that handles the sending of
    #  camera frames for each connection that is established
    def __server_listen(self, device):

        self.__streaming = True

        while self.__streaming:
            self.__socket.listen()
            conn, addr = self.__socket.accept()
            if not self.connections:
                thread = threading.Thread(target=self.__stream)
                thread.start()
            self.connections.append(conn)


    ## \brief Encode and stream video.
    #
    #  Capture and encode camera frames in order to send them via the streaming socket
    def __stream(self):

        while self.__streaming:

            try:
                ret, frame = self.__cam.read()
                ret, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                data = pickle.dumps(frame, 0)
                size = len(data)

                try:
                    # if one connection fails, closes all of them
                    for i in range(len(self.connections)):
                        self.connections[i].sendall(struct.pack('>L', size) + data)

                except:
                    self.stop_stream()  
            except:
                time.sleep(0.1)

        self.__cleanup()

    ## \brief Stop streaming.
    #
    #  Stops and closes the streaming server
    def stop_stream(self):

        if self.__streaming:
            self.__streaming = False
            closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closer.connect((self.__host, self.__port))
            closer.close()
            self.__cleanup()

            for conn in self.connections:
                conn.close()

            self.connections = []

            self.__socket.close()

        else:
            print("O servidor não está realizando o streaming")
