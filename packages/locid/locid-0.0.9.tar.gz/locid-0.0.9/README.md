# LOC.id Python bindings

Library for interacting with locid devices over serial adapters (/LOC.id USB-dongles) and bluetooth.

## Installation

**Directly from GitLab (master)**

```shell
pip install git+ssh://git@git.rtb-bl.de/ampel/locid/locid-py.git
```

**Pypi**

```shell
pip install locid
```

_(Deployed from time to time for customers / third party integrations, see [pypi locid](https://pypi.org/project/locid/#history))_.

## Command line utility

When installed via pip, locid-py installs a little command line utilty. 

Execute `locid -h` for a list of supported commands.

## Usage / Examples

- [(USB-)Serial/UART Example](/example_locid_dongle.py) (Nordic USB-Dongle)
- [Bluetooth Example](/example_bluetooth_hci.py) (Regular Bluetooth Adapter / HCI)

## Integration

### As a git submodule

To integrate locid-py directly in your project, navigate to the directory or your project's python scripts and execute:

```shell
git submodule add git@git.rtb-bl.de:ampel/locid/locid-py.git
```

Inside your scripts, you can include the library as follows:

```python
import sys
import os

# add locid python bindings from subdirectory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "locid-py"))
from locid.ble import *

async with LocIdBleClient(BLE_MAC) as locid:
    await locid.jsonrpc_request("locid.ping")
```

### In requirements.txt

Add in your requirements.txt

```
pyserial
# ...

git+ssh://git@git.rtb-bl.de/ampel/locid/locid-py.git
```

Then use the standard way to install your requirements:

```shell
pip install -r requirements.txt
```

## Firmware

Firmware (for Nordic/Laird USB Dongles) is available from [LOC.id BLE Archive (master)](https://git.rtb-bl.de/ampel/locid/RTB_LOC.id/-/jobs/artifacts/master/download?job=build). Download, extract & install from `build-usb/src` folder.
