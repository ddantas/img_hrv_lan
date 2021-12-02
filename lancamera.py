import cv2
import threading
import socket
import pickle
import struct
from scapy.all import *

class LanCamera:


    def __init__(self, HOST='127.0.0.1', PORT=9000):
    
        self.__running = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def list_servers(self, port_range: list):

        hosts = self.__scan_ports(port_range)
        if len(hosts) > 0:
            print("Servidores encontrados: ")
            for host, ports in hosts.items():
                print(f"IP Servidor: {host}; Portas abertas: {ports}")
        else:
            print("Nenhum servidor foi encontrado")

    def __scan_ports(self, port_range: list):

        if type(port_range) is int:
            start = port_range
            end = start
        else:
            start = port_range[0]
            end  = port_range[1]

        ips = self.__get_ips()
        hosts = {}
        for ip in ips:
            ports = []
            print(f"Scaneando portas {start}-{end} do host {ip}")
            for port in range(start, end):
                if self.__scan_port(ip, port):
                    ports.append(port)

            hosts[ip] = ports

        return hosts

    def __scan_port(self, ip, port, timeout=2):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        if s.connect_ex((ip, port)) == 0:
            s.close()
            return True

        s.close()
        return False

    def __get_ips(self, network='192.168.1.0/24'):

        ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network),timeout=2)
        ips = []
        for res in ans.res:
            ips.append(res.answer.psrc)
        return ips

    def list_cams_local(self, num):

        # lista as cameras de num ate 0
        index = 0
        v = []
        i = num
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                v.append(index)
                cap.release()
                
            index += 1
            i -= 1
        return v

    def list_cams_lan(self):
        pass


class Client(LanCamera):

    def __init__(self, HOST='127.0.0.1', PORT=9000):

        self.__running = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self, record=False):

        if self.__running: 
            print("O cliente já está rodando")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__connect, args=(record, ))
            server_thread.start()

    def __connect(self, record):

        self.__socket.connect((self.__host, self.__port))
        self.__connected = True
        thread = threading.Thread(target=self.__handle_conn, args=(record, ))
        thread.start()

    def __handle_conn(self, record):

        if record:
            cod = cv2.VideoWriter_fourcc(*'MJPG')
            vidWriter = cv2.VideoWriter('media/camera_client.mp4',cod,30.0,(640,480))

        data = b''
        img_data_size = struct.calcsize('>L')
        while self.__running:
            quit = False

            while len(data) < img_data_size:
                recv = self.__socket.recv(4096)
                data += recv
                if data == b'':
                    self.__socket.close()
                    quit = True
                    break
            if quit:
                break

            msg_size = data[:img_data_size]
            data = data[img_data_size:]

            msg_size = struct.unpack(">L", msg_size)[0]

            while len(data) < msg_size:
                data += self.__socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]  
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if record:
                vidWriter.write(frame)

            cv2.imshow(str(self.__host), frame)

            if cv2.waitKey(1) == ord('q'):
                self.__socket.close()
                break


    def stop_client(self):

        if self.__running:
            self.__running = False
            self.__socket.close()

        else:
            print("Não tem clientes rodando")

class Server(LanCamera):

    def __init__(self, HOST='127.0.0.1', PORT=9000, device=0):
    
        self.__running = False
        self.__host = HOST
        self.__port = PORT
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__cam = None
        self.__init_camera(device)
        self.__init_socket()

    def __init_socket(self):
        self.__socket.bind((self.__host, self.__port))

    def __init_camera(self, device):
        self.__cam = cv2.VideoCapture(device)

    def __cleanup(self):
        self.__cam.release()
        cv2.destroyAllWindows()

    def start_stream(self, record=False):

        if self.__running:
            print("O servidor já está realizando o streaming")

        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listen, args=(record, ))
            server_thread.start()

    def __server_listen(self, record):
        self.__socket.listen()
        conn, addr = self.__socket.accept()
        thread = threading.Thread(target=self.__stream, args=(conn, record, ))
        thread.start()

    def __stream(self, conn, record):

        if record:
            size = (int(self.__cam.get(3)), int(self.__cam.get(4)))
            vidWriter = cv2.VideoWriter('media/camera_server.mp4', cv2.VideoWriter_fourcc(*'MJPG'), 30, size)

        while self.__running:
            ret, frame = self.__cam.read()
            if record:
                vidWriter.write(frame)
            ret, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                conn.sendall(struct.pack('>L', size) + data)

            except:
                self.__running = False

        self.__cleanup()

    def stop_stream(self):

        if self.__running:
            self.__running = False
            closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closer.connect((self.__host, self.__port))
            closer.close()
            self.__socket.close()

        else:
            print("O servidor não está realizando o streaming")
