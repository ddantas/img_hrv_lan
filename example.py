from lancamera import *
import time

# HOST and PORT parameters are optional default: HOST='127.0.0.1', PORT=9000
server = Server(HOST='127.0.0.1', PORT=9000)
client = Client(HOST='127.0.0.1', PORT=9000)

""" start_stream starts to listen on the class socket and accepts the first connection
 after the connection is established, opens the camera, encodes the frames and sends
them via the socket """
# record parameter is optional, it saves the frames on the disk
server.start_stream(record=False)

""" start_connection tries to use the class socket to connect to HOST and PORT
 after the connection is established, receives the data, decodes it and shows it on the screen
"""
client.start_connection(record=False)

time.sleep(10)

# closes the connections
server.stop_stream()
client.stop_client()
# --------------------------
lan = LanCamera()
""" list_server lists all hosts available on LAN that have an open port in the range specified """
lan.list_servers([80, 90])
