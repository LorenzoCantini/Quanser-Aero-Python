<h1>Quanser Aero Python</span></h1>

Python product application library for Quanser Aero 

## Overview

Quanser Aero is a learning tool developed and distributed by Quanser Consulting Inc.

<img src="assets/aero.png" width="20%" style="max-width: 522px"><br/>

This repository contains code for a Python interface to control Quanser Aero. 

## Usage
Download [our Quanser Aero interface](quanseraero/aero.py) in your project folder and simply import it with:

```py
from aero import Aero
```

Then use it in your code like this:
```py
with Aero() as aero:

    aero.write_led(np.array([0, 1, 0], dtype=np.float64))

    aero.read_analog_encoder_other_channels()

    if aero.pitchAngle > 0:
        aero.write_voltage(0, -10)
```

## Requirements

To use this library, you need to install [numpy](https://numpy.org/) and the [Quanser Python API](https://docs.quanser.com/quarc/documentation/python/getting_started.html).

## Contributing

You are very welcome to contribute to this project. Feel free to open an issue or pull request if you have any suggestions or bug reports.

[Quanser Aero documentation](https://docs.quanser.com/quarc/documentation/quanser_aero_usb.html)

## License

This project is licensed under the BSD 3-Clause License - see the `LICENSE` file for details. Note that the repository relies on third-party code, which is subject to their respective licenses.
