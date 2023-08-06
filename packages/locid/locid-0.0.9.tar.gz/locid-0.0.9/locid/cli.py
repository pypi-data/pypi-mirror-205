#!/usr/bin/env python3

import sys
import inspect
import asyncio
import argparse
import time
import json

from .ble import *
from .ble import LocIdBle
from .locid import LocIdUSBDongle


async def main_async():

    parser = argparse.ArgumentParser(
                    prog='locid',
                    description='locid command line utility')

    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.add_parser('hci-ble-scan', help="Bluetooth scan & dump nearby locid devices (using HCI adapter)")
    subparsers.add_parser('watch-state', help="Watches state (polling)")
    parser_usb = subparsers.add_parser('raw-exec', help="Runs methods on USB-Dongle from command line (e.g. 'restart')")
    subparsers.add_parser('raw-event-dump', help="Dumps raw events")
    subparsers.add_parser('mesh-state', help="Dumps state of mesh/net2")
    subparsers.add_parser('mesh-scan', help="Scans for mesh/net2 devices in network")

    parser_usb.add_argument("method")
    parser_usb.add_argument("params", nargs="*")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    # print("argparse res:", args)

    if args.cmd == "ble-scan":
        await LocIdBle.scan_print(timeout=30)
        return

    elif args.cmd == 'raw-exec':
        with LocIdUSBDongle() as dev:
            v = dev.getVersion()["version"]
            print(f"USB Dongle fw version: {v}")
            print(f"Beacon ID: {dev.getBeaconId().get('id'):#0{8}x}")

            # print("available dongle methods:", dir(l))

            method_name = args.method
            try:
                method = getattr(dev, method_name)
            except AttributeError:
                print("no such method: ", method_name)
                sys.exit(1)

            sig = inspect.signature(method)
            print("signature:", sig)

            params = args.params

            params_t = []
            for i, p in enumerate(params):
                sigp = list(sig.parameters.values())[i]
                type = sigp.annotation
                if type == int:
                    params_t.append(int(p))
                else:
                    params_t.append(p)

            print("params after map:", params_t)

            res = method(*params_t)
            print("result:", res)

    elif args.cmd == "raw-event-dump":
        with LocIdUSBDongle() as dev:

            def on_notification(n):
                print("Raw notification:", n)
            dev.on_notification(on_notification)

            while True:
                time.sleep(1)

    elif args.cmd == "watch-state":
        with LocIdUSBDongle() as dev:

            def on_notification(n):
                print("notification: ", n)

            dev.on_notification(on_notification)

            v = dev.getVersion()["version"]
            print(f"USB Dongle firmware version: {v}")

            while True:
                s = dev.getStatus()
                print(s)
                time.sleep(1)

    elif args.cmd == "mesh-state":
        with LocIdUSBDongle() as dev:
            r = dev.jsonrpc_call("mesh.getStatus")
            print(json.dumps(r, indent=4))

    elif args.cmd == "mesh-scan":
        with LocIdUSBDongle() as dev:

            def on_notification(n):
                # print("notification: ", n)
                pass

            dev.on_notification(on_notification)

            print("Requesting meta information...")
            dev.jsonrpc_call("mesh.requestMeta")

            time.sleep(5)

            nodes_res = dev.jsonrpc_call("mesh.getNodes")

            for n in nodes_res['nodes']:
                addr = n['addr']
                node_stats = dev.jsonrpc_call("mesh.getNodeStats", {"addr": addr})
                print("*" * 100)
                print("mesh node:", json.dumps(node_stats, indent=4))


def main():
    """entry point (when installed by pip as script)"""
    asyncio.run(main_async())
