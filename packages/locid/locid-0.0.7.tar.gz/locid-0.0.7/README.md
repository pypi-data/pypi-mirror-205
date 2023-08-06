# LOC.id Python bindings

Library for interacting with locid devices over serial adapters (/LOC.id USB-dongles) and bluetooth.

(Note: A public (stripped down version) fork for customers is available at [locid-py-pub](https://git.rtb-bl.de/ampel/locid/locid-py))

## Installation

**Directly from git**

```shell
pip install git+https://git.rtb-bl.de/ampel/locid/locid-py.git
```

## Command line utility

When installed via pip, locid-py installs a little command line utilty. 

Execute `locid -h` for a list of supported commands.

## Usage / Examples

- [(USB-)Serial/UART Example](/example.py) (Nordic USB-Dongle)
- [Bluetooth Example](/example_bluetooth.py) (Regular Bluetooth Adapter / HCI)

## Integration

### As a git submodule

To integrate locid-py directly in your project, navigate to the directory or your project's python scripts and execute:

```shell
git submodule add git@git.rtb-bl.de:ampel/locid/locid-py.git
```

Inside your scripts, you can include the library as follows:

```python
import sys

# add locid python bindings from subdirectory
sys.path.insert(0, "locid-py")
from locid.ble import *

async with LocIdBleClient(BLE_MAC) as locid:
    await locid.jsonrpc_request("locid.ping")
```

### In requirements.txt

Add in your requirements.txt

```
pyserial
# ...

git+https://git.rtb-bl.de/ampel/locid/locid-py.git
```

Then use the standard way to install your requirements:

```shell
pip install -r requirements.txt
```




