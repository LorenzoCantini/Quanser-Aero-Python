from quanser.hardware import HIL, HILError, Clock
import numpy as np

WRITE_OTHER_CHANNELS = np.array([11000, 11001, 11002], dtype=np.uint32)

red = np.array([1,0,0],dtype=float)
green = np.array([0,1,0],dtype=float)
blue = np.array([0,0,1],dtype=float)

try:
    aero=HIL("quanser_aero_usb", '0')

    aero.write_other(WRITE_OTHER_CHANNELS, 3, green)
    
    methods = [func for func in dir(aero) if callable(getattr(aero, func)) and not func.startswith("__")]
    attributes = [attr for attr in dir(aero) if not callable(getattr(aero, attr)) and not attr.startswith("__")]
    
    for i in methods: print(i, getattr(aero, i).__doc__, "~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(attributes)
    
    input("Press key to end...")
    aero.write_other(WRITE_OTHER_CHANNELS, 3, red)
    aero.close()
    
except Exception as e:
    aero.write_other(WRITE_OTHER_CHANNELS, 3, red)
    aero.close()
    print(e)