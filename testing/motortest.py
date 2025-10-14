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

# motor
MAX_MOTOR_INPUT = 999

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

def write_voltage(device, voltage0=0, voltage1=0):
    """
    Writes voltage commands to the motors on the Aero2.

    Parameters
    ----------
    voltage0 : float
        Voltage command sent to rotor 0. Must be between -999 and 999.
    voltage1 : float
        Voltage command sent to rotor 1. Must be between -999 and 999.
    """
    try:
        writeAnalogBuffer = np.array([np.clip(voltage0, -MAX_MOTOR_INPUT, MAX_MOTOR_INPUT), np.clip(voltage1, -MAX_MOTOR_INPUT, MAX_MOTOR_INPUT)], dtype=np.float64)

        device.write_analog(WRITE_ANALOG_CHANNELS, len(WRITE_ANALOG_CHANNELS), writeAnalogBuffer)

    except HILError as h:
        print(h.get_error_message())

try:
	aero=HIL("quanser_aero_usb", '0')
	aero.write_other(WRITE_OTHER_CHANNELS, len(WRITE_OTHER_CHANNELS), green)
	aero.write_digital(WRITE_DIGITAL_CHANNELS, len(WRITE_DIGITAL_CHANNELS), writeDigitalBuffer) # initialize motor

	try: 
		write_voltage(aero, 0, 0)
		time.sleep(1)
		read_sensors(aero)
		input(f"Press ENTER to start motor tryout")

	except KeyboardInterrupt:
		pass

	try: 
		write_voltage(aero, 0, 0)
		while True:
			read_sensors(aero)
			print(f"Motor speed: [{2*np.pi*readOtherBuffer[6]/2048: 04.0f} {2*np.pi*readOtherBuffer[7]/2048: 04.0f}] rad/s")
			print(f"Motor current: [{readAnalogBuffer[0]: 06.3f} {readAnalogBuffer[1]: 06.3f}] A")
			print("Insert motor commands (between -999 and 999) or 'q' to quit")
			cmd = input()
			if cmd=='q':
				break
			elif len(cmd) == 0:
				time.sleep(2)
				continue
			elif not cmd.isdigit() and not (cmd[0]=='-' and cmd[1:].isdigit()):
				print("Invalid command")
				time.sleep(2)
				continue
			cmd = int(cmd)
			write_voltage(aero, cmd, cmd)
			time.sleep(2)

	except KeyboardInterrupt:
		pass

	aero.write_other(WRITE_OTHER_CHANNELS, 3, red)
	write_voltage(aero, 0, 0)
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
	write_voltage(aero, 0, 0)
	aero.close()
	print("Exception caught: ", e)