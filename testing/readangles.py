from quanser.hardware import HIL, HILError, Clock
import numpy as np
import time

# read channels
READ_ANALOG_CHANNELS = np.array([0, 1], dtype=np.uint32)
READ_ENCODER_CHANNELS = np.array([0, 1, 2, 3], dtype=np.uint32)
READ_OTHER_CHANNELS = np.array([3000, 3001, 3002, 4000, 4001, 4002, 14000, 14001, 14002, 14003], dtype=np.uint32)

# write channels
WRITE_ANALOG_CHANNELS = np.array([0, 1], dtype=np.uint32)
WRITE_DIGITAL_CHANNELS = np.array([0, 1], dtype=np.uint32)
WRITE_OTHER_CHANNELS = np.array([11000, 11001, 11002], dtype=np.uint32)

red = np.array([1,0,0],dtype=float)
green = np.array([0,1,0],dtype=float)
blue = np.array([0,0,1],dtype=float)

# read buffers (internal)
readAnalogBuffer = np.zeros(2, dtype=np.float64)
readEncoderBuffer = np.zeros(4, dtype=np.int32)
readOtherBuffer = np.zeros(10, dtype=np.float64)

# write buffers
writeAnalogBuffer = np.array([10, 10], dtype=np.float64)
writeDigitalBuffer = np.array([1, 1], dtype=np.int8)
writeOtherBuffer = np.array([1, 0, 0], dtype=np.float64)

def read_sensors(device):
	device.read(READ_ANALOG_CHANNELS, len(READ_ANALOG_CHANNELS), READ_ENCODER_CHANNELS, len(READ_ENCODER_CHANNELS), 
	None, 0, 
	READ_OTHER_CHANNELS, len(READ_OTHER_CHANNELS), readAnalogBuffer, readEncoderBuffer, 
	None, readOtherBuffer)

try:
	aero=HIL("quanser_aero_usb", '0')

	aero.write_other(WRITE_OTHER_CHANNELS, 3, green)

	input("Press enter to start reading angles (in [rad])")
	print("ctrl+C to quit")

	try:
		# reset the encoder count, so sets the angle at zero at the current position
		aero.set_encoder_counts(READ_ENCODER_CHANNELS, len(READ_ENCODER_CHANNELS), np.array([0, 0, 0, 0], dtype=np.float64))
		
		while True:
			read_sensors(aero)
			print(f"Pitch: {2*np.pi*readEncoderBuffer[2]/2048: 06.2f}, Yaw: {2*np.pi*readEncoderBuffer[3]/4096: 06.2f}")
			time.sleep(1)
	
	except KeyboardInterrupt:
		pass

	aero.write_other(WRITE_OTHER_CHANNELS, 3, red)
	aero.close()

except HILError as e:
	try:
		aero.close()
	except:
		pass
	print("HIL Exception caught: ", e)
	print(e.get_error_message())

except Exception as e:
	aero.write_other(WRITE_OTHER_CHANNELS, 3, red)
	aero.close()
	print("Exception caught: ", e)
	if hasattr(e, 'get_error_message'):
		print(e.get_error_message())