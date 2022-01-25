import struct
import Data

class Packet:
	def __init__(self, tp, content):
		self.tp = int(tp)
		self.content = content

	def construct_packet(self):

		packet_type = struct.pack('c', str(self.tp).encode())
		packet_bytes = self.content.encode()
		packet_len = struct.pack('i', len(self.content))

		return packet_type + packet_len + packet_bytes

	def read_packet(self, packet):

		packet_type = packet[0]
		size_int = struct.calcsize('i')
		packet_len = packet[1:size_int]
		packet_bytes = packet[size_int:]

		self.type = packet_type
		self.content = packet_bytes
		self.len = packet_len

	def decode_packet(self):

		self.content = self.content.replace('[','')
		self.content = self.content.replace(']','')

		print('decoding', self.tp, type(self.tp), Data.TYPE_ECG)

		if self.tp == Data.TYPE_ECG:
			data = Data.Data(Data.TYPE_ECG)
			values_time, values_timestamp, values_ecg = self.content.split(';')

			values_time = [float(v) for v in values_time.split(',')]
			values_timestamp = [int(v) for v in values_timestamp.split(',')]
			values_ecg = [int(v) for v in values_ecg.split(',')]

			data.time = values_time
			data.timestamp = values_timestamp
			data.values_ecg = values_ecg

		else:
			data = Data.Data(Data.TYPE_RR)
			values_time, values_hr, values_rr = self.content.split(';')

			values_time = [float(v) for v in values_time.split(',')]
			values_hr = [int(v) for v in values_hr.split(',')]
			values_rr = [int(v) for v in values_rr.split(',')]

			data.time = values_time
			data.values_hr = values_hr
			data.values_rr = values_rr

		return data

