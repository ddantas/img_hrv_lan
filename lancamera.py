import cv2
import threading
import socket
import pickle
import struct
import scapy.all as sp
import time
from PIL import Image
from PIL import ImageTk

## @package lancamera
#  This package exposes the functionalities of the cameras
#  available in the LAN.

PORT_CAM   = 9000
PORT_POLAR = 9001
PORT_COMMANDS = 9002

## \brief Class LanCamera
#
#  Main class of the package lancamera, with functionalities to list camera servers and their cameras.
class LanCamera:

    def __init__(self):    
        self.cam = None

    ## \brief Initialize camera
    #
    #  Initializes video capture device
    def init_camera(self, device):
        self.cam = cv2.VideoCapture(device)

    ## \brief Destroy camera
    #
    #  Destroy video capture device and window data structures
    def cleanup(self):
        if self.cam:
            self.cam.release()
            cv2.destroyAllWindows()

    ## \brief List all cameras in localhost.
    #
    #  List all the available capture devices with index up to 'num' in localhost .
    def list_cams_local(self, num=5):

        v = []
        i = 0
        while i < num:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                v.append(i)
                cap.release()
            i += 1
        return v

## \brief Class Client
#
#  Class with functionalities to query and connect to camera servers.
class Client(LanCamera):

    def __init__(self, HOST='0.0.0.0', PORT=PORT_CAM, name=''):

        self.__running = False
        self.__streaming = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_commands = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = b''

    """#########################################################
    ############################################################
    ###              NETWORK FUNCTIONALITIES                 ###
    ############################################################
    #########################################################"""

    ## \brief Set the internal host ip and port.
    #
    #  Set the internal host ip and port that the client will use 
    #  to connect to the server.
    def set_host(self, host, port):
        self.__host = host
        self.__port = port

    ## \brief List servers listening to a given port.
    #
    #  List all available servers on LAN that have certain ports open.
    #  The opened ports should belong to the list 'ports_to_scan'.
    def list_servers(self, ports_to_scan):

        hosts = self.__list_lan_ports(ports_to_scan)

        if len(hosts) > 0:
            print("Servidores encontrados: ")
            for host, ports in hosts.items():
                print(f"IP Servidor: {host}; Portas abertas: {ports}")
        else:
            print("Nenhum servidor foi encontrado")

        return hosts

    ## \brief List specific host listening to a given port.
    #
    #  Check if the specified host has certain ports open.
    def list_host_at(self, ip, ports_to_scan):
        return self.__list_server_ports(ip, ports_to_scan)

    ## \brief List cameras from a single host.
    #
    #  List all cameras from a specified host.
    #  list devs, specify only the type of device
    def list_cams_at(self, ip, ports_to_scan=[9000,9002]):

        ports = self.list_host_at(ip, ports_to_scan)
        devices = []
        if set(ports) == set(ports_to_scan):
            devices = self.recv_cameras(ip, PORT_COMMANDS)

        return devices

    ## \brief List cameras from available hosts in the network.
    #
    #  List all cameras and hosts with available cameras in the LAN.
    def list_cams_lan(self, ports_to_scan=[9000,9002]):

        hosts = self.list_servers(ports_to_scan)
        devices = {}
        for ip, ports in hosts.items():
            if set(ports) == set(ports_to_scan):
                cams = self.recv_cameras(ip, PORT_COMMANDS)
                devices[ip] = cams

        return devices

    ## \brief List open ports of the hosts in the LAN.
    #
    # For each ip obtained through __get_ips(), determines which port, in 'ports_to_scan' is open.
    def __list_lan_ports(self, ports_to_scan):

        ips = self.__get_ips()
        ips.append("127.0.0.1")
        hosts = {}
        for ip in ips:
            ports = self.__list_server_ports(ip, ports_to_scan)
            print(f"Scaneando portas {ports_to_scan} do host {ip}")

            if ports:
                hosts[ip] = ports

        return hosts

    ## \brief List open ports of a specific host.
    #
    # For a single ip, determines which port, in 'ports_to_scan' is open.
    def __list_server_ports(self, ip, ports_to_scan):

        if type(ports_to_scan) is int:
            ports_to_scan = [ports_to_scan]

        ports = []
        for port in ports_to_scan:
            if self.__scan_port(ip, port):
                ports.append(port)

        return ports

    ## \brief Tries to connect to a port of an IP address.
    #
    #  Tries to connect to a specific port and IP to see if the port is open
    def __scan_port(self, ip, port, timeout=2):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        if s.connect_ex((ip, port)) == 0:
            # s.sendall(b'END')
            s.close()
            return True

        s.close()
        return False

    ## \brief Get all hosts in the LAN.
    #
    #  Pings via ARP protocol all hosts in the network to obtain the IPs of available hosts in the network
    #  (MUST RUN AS ROOT TO PING VIA ARP)
    #
        #  Uncomment this to debug.
    #def get_ips(self, network='192.168.0.0/24'):
    #    return self.__get_ips(network)
    def __get_ips(self, network='192.168.0.0/24'):

        ans,unans = sp.srp(sp.Ether(dst="ff:ff:ff:ff:ff:ff")/sp.ARP(pdst=network),timeout=2)
        ips = []
        for res in ans.res:
            ips.append(res.answer.psrc)

        return ips

    ## \brief Receive a list of all open cameras on a host.
    #
    #  Queries the host for its open cameras and parses the response to group them in a list.
    def recv_cameras(self, ip, port):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            msg_len = struct.pack('i', len('LIST'))
            s.sendall(msg_len + b"LIST")
            cams = s.recv(1024).decode()
            cams = cams.replace(' ', '')
            cams = cams.replace('[','')
            cams = cams.replace(']','')
            cams = cams.split(',')
            # for cam in cams:
            #     devices.append(cam)
            print(f'Cameras do servidor {ip}:9000 -> {cams}')
            msg_len = struct.pack('i', len('END'))
            s.sendall(msg_len + b"END")

        return cams

    """#########################################################
    ############################################################
    ###             COMMANDS FUNCTIONALITIES                 ###
    ############################################################
    #########################################################"""

    ## \brief Connects to a commands server.
    #
    #  Starts a thread that does the connection with the commands server
    def start_commands_connection(self):

        if self.__running:
            print("O cliente já está conectado")
        else:
            self.__running = True
            self.__socket_commands.connect((self.__host, self.__port + 2))

    ## \brief Sends a command to the server.
    #
    #  Sends the specified command to the server
    def send_command(self, command):

        msg_len = struct.pack('i', len(command))
        self.__socket_commands.sendall(msg_len + command.encode())

    ## \brief Stop connection.
    #
    #  Stop the client connection to the commands server
    def stop_commands_client(self):

        if self.__running:
            self.__running = False
            self.__socket_commands.close()

        else:
            print("Não tem clientes rodando")

    """#########################################################
    ############################################################
    ###         CAMERA STREAMING FUNCTIONALITIES             ###
    ############################################################
    #########################################################"""

    ## \brief Connects to a streaming server.
    #
    #  Starts a thread that does the connection with the streaming server
    def start_streaming_connection(self):

        if self.__streaming: 
            print("O cliente já está rodando")
        else:
            self.__streaming = True
            self.__socket.connect((self.__host, self.__port))

    ## \brief Receives frame from the server.
    #
    #  Receives, decodes and displays a single streaming frame that was received from the server
    #  This method is designed to be accessed by the GUI interface in order to display
    #  the frame on the application window
    def recv_frame(self, img_data_size):

        # self.__socket.send(b'READY')
        while len(self.data) < img_data_size:
            recv = self.__socket.recv(4096)
            self.data += recv

            if self.data == b'':
                self.stop_streaming_client()
                return None

        msg_size = self.data[:img_data_size]
        self.data = self.data[img_data_size:]

        msg_size = struct.unpack(">L", msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.__socket.recv(4096)
            if self.data == b'':
                self.stop_streaming_client()
                return None
            
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]  
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        return frame

    ## \brief Stop connection.
    #
    #  Stop the client connection to the streaming server
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

    def __init__(self, HOST='', PORT=PORT_CAM, device=0):
        
        super().__init__()
        self.__running = False
        self.__streaming = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_commands = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cam = None
        self.connections = []
        self.__init_socket()

    ## \brief Initialize socket
    #
    #  Initializes all sockets binding them to specific ports
    def __init_socket(self):
        self.__socket.bind((self.__host, self.__port))
        self.__socket_commands.bind((self.__host, self.__port + 2))

    """#########################################################
    ############################################################
    ###             COMMANDS FUNCTIONALITIES                 ###
    ############################################################
    #########################################################"""

    ## \brief Receives command
    #
    #  First, receives the number of bytes of that command (size), 
    #  then receives the proper command
    def recv_command(self, conn):
        n_bytes = conn.recv(struct.calcsize ('i'))
        size = struct.unpack('i', n_bytes)[0]
        return conn.recv(size)

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

            if self.__running:
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
                data = self.recv_command(conn)
            except:
                break

            if data == b"LIST":

                cams = self.list_cams_local(5)
                try:
                    conn.sendall(str(cams).encode())
                except:
                    break

            if b'ROUTINE' in data:

                host = data.split(b';')[1].decode()
                print(host)
                cur_time = 0

                size = struct.unpack('i', conn.recv(struct.calcsize ('i')))[0]
                routine = conn.recv(size).decode()
                lines = routine.split('\n')

                for line in lines:
                    cmds = line.split(';')
                    instant, cmd, hosts, instruction = cmds
                    instant = instant.strip()
                    cmd = cmd.strip()
                    hosts = hosts.strip()
                    instruction = instruction.strip()
                    instruction = instruction.replace('“', '')
                    instruction = instruction.replace('”', '')
                    instant = float(instant)

                    if instant - cur_time > 0:
                        time.sleep(instant - cur_time)
                        cur_time += instant - cur_time

                    if hosts == 'all':
                        hosts = ['s1', 's2']

                    if host in hosts:
                        routine_handler(cmd, instruction)

            if b'SELECT' in data:
                device = int(data.split(b' ')[1])
                try:
                    self.init_camera(device)

                except:
                    print("Erro ao selecionar camera")

            if data == b'END' or data == b'':
                break

        conn.close()

    ## \brief Stop command server thread
    #
    #  Stop the server that is waiting for connections to execute commands
    def stop_commands_server(self):

        if self.__running:
            self.__running = False

            closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closer.connect((self.__host, self.__port + 2))
            closer.close()
            self.__socket_commands.close()

        else:
            print("O servidor não está realizando o streaming")

    """#########################################################
    ############################################################
    ###           CAMERA STREAMING FUNCTIONALITIES           ###
    ############################################################
    #########################################################"""

    ## \brief Start video streaming thread.
    #
    #  Starts a thread to listen for connections for video streaming
    def start_stream_server(self):

        if self.__streaming:
            print("O servidor já está realizando o streaming")
            return

        server_thread = threading.Thread(target=self.__server_listen)
        server_thread.start()

    ## \brief Listen to streaming requisitions.
    #
    #  Listens for an incoming connection and starts a thread that handles the sending of
    #  camera frames for each connection that is established
    def __server_listen(self):

        self.__streaming = True

        while self.__streaming:
            self.__socket.listen()
            conn, addr = self.__socket.accept()

            ''' if we are closing the server (self.__streaming was set to False while accept() was waiting)
                we don't want to start anything else '''
            if self.__streaming:

                if self.connections == []:
                    thread = threading.Thread(target=self.__stream)
                    thread.start()

                self.connections.append(conn)


    ## \brief Encode and stream video.
    #
    #  Capture and encode camera frames in order to send them via the streaming socket
    def __stream(self):

        while self.__streaming:

            if self.cam:
                ret, frame = self.cam.read()

                if ret:
                    ret, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                    data = pickle.dumps(frame, 0)
                    size = len(data)

                    try:
                        # if one connection fails, stops the server entirely
                        if self.__streaming:
                            for conn in self.connections:
                                # ready = conn.recv(1024)
                                # if ready == b'READY':
                                conn.sendall(struct.pack('>L', size) + data)

                    except:
                        self.connections.remove(conn)

                else:
                    break
            else:
                time.sleep(0.1)

    ## \brief Stop streaming.
    #
    #  Stops and closes the streaming server
    def stop_stream(self):

        if self.__streaming:

            self.__streaming = False

            closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            closer.connect((self.__host, self.__port))
            closer.close()

            self.__socket.close()
            self.connections = []

            self.cleanup()

        else:
            print("O servidor não está realizando o streaming")


"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""


if __name__ == "__main__":
  c = LanCamera()
  cams = c.list_cams_local()
  print("Local cameras: %s" % cams)
  c.list_servers((PORT_CAM))

  server = Server(HOST='0.0.0.0', PORT=9000)
  client = Client(HOST='127.0.0.1', PORT=9000)
