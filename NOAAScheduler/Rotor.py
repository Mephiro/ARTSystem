import time
import serial

class Rot2proG:

	pulse = 0
	debug = False
	max_az = float(360)
	min_az = float(-180)
	max_el = float(180)
	min_el = float(0)
	dev_path = ''

	def __init__(self, serial_port):
		self.dev_path = serial_port
		self.ser = serial.Serial(port=self.dev_path, baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		print(str(self.ser.name))
		self.status()

	def __del__(self):
		self.ser.close()

	def status(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x1f', '\x20']
		packet = "".join(cmd)
		
		self.ser.write(bytes(packet,'utf-8'))
		self.ser.flush()

		rec_packet = self.ser.read(12)

		az = (rec_packet[1]*100) + (rec_packet[2]*10) + rec_packet[3] + (rec_packet[4]/10) - 360.0
		el = (rec_packet[6]*100) + (rec_packet[7]*10) + rec_packet[8] + (rec_packet[9]/10) - 360.0
		ph = rec_packet[5]
		pv = rec_packet[10]

		ret = [az, el, ph]

		assert(ph == pv)
		self.pulse = ph
		return ret

	def stop(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x0f', '\x20']
		packet = "".join(cmd)

		self.ser.write(bytes(packet,'utf-8'))
		self.ser.flush()

		rec_packet = self.ser.read(12)

		az = (rec_packet[1]*100) + (rec_packet[2]*10) + rec_packet[3] + (rec_packet[4]/10) - 360.0
		el = (rec_packet[6]*100) + (rec_packet[7]*10) + rec_packet[8] + (rec_packet[9]/10) - 360.0
		ph = rec_packet[5]
		pv = rec_packet[10]

		ret = [az, el, ph]

		assert(ph == pv)
		self.pulse = ph
		return ret

	def set(self, azi, eli):

		assert(float(azi) <= self.max_az)
		assert(float(azi) >= self.min_az)
		assert(float(eli) <= self.max_el)
		assert(float(eli) >= self.min_el)

		az = "0" + str(int(self.pulse * (float(azi) + 360)))
		el = "0" + str(int(self.pulse * (float(eli) + 360)))

		cmd = ['\x57', az[-4], az[-3], az[-2], az[-1], chr(self.pulse), el[-4], el[-3], el[-2], el[-1], chr(self.pulse), '\x2f', '\x20']
		packet = "".join(cmd)

		self.ser.write(bytes(packet,'utf-8'))
		self.ser.flush()

		time.sleep(1)
