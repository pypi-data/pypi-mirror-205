#!/usr/bin/env python3
"""
see https://git.rtb-bl.de/ampel/acoustic/blx-doc/-/blob/master/README.md
"""

import os
import binascii
import crcmod
import struct
import io
import logging

crc_fun = None

logging.basicConfig(level=1)

# CRC16-XMODEM
crc_fun = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
assert crc_fun(b'123456789') == 0x31C3, "something is wrong with the crc algo"


def rtb_serial_protocol_encode(header_preamble: str,
                               command_class: str,
                               command: str,
                               data: bytes = None) -> bytes:
    global crc_fun

    if not data:
        data = bytearray()

    res = bytearray(b'#')

    if isinstance(header_preamble, str):
        header_preamble = header_preamble[0].encode('ascii')
    res += header_preamble

    header_data_second_layer_length = 2 + 2 + len(data)

    # size of payload (2 bytes)
    res += (header_data_second_layer_length).to_bytes(2, byteorder='little')

    header_crc = crc_fun(res)
    res += header_crc.to_bytes(2, 'big')
    # print("gen header crc:", header_crc)

    if isinstance(command_class, str):
        command_class = command_class[0].encode('ascii')
    elif isinstance(command_class, int):
        command_class = bytes([command_class])
    if isinstance(command, str):
        command = command[0].encode('ascii')
    elif isinstance(command, int):
        command = bytes([command])

    res += command_class
    res += command
    res += data

    payload_crc = crc_fun(res[6:])
    res += payload_crc.to_bytes(2, 'big')
    # print("gen payload crc:", payload_crc)

    return res


def rtb_serial_protocol_parse(io_in, skip_to_start_byte=True):
    """
    Generator for parsing serial protocol packets from io streams
    """

    global crc_fun
    print("rtb_serial_protocol_parse")

    if "SKIP" in os.environ:
        io_in.seek(int(os.environ['SKIP']))

    while True:
        s = io_in.read(1)
        if len(s) == 0:
            print('end of file')
            break

        if skip_to_start_byte and s != b"#":
            # print("skipping byte (waiting for #):", s)
            continue

        preamble = io_in.read(1)

        # header data is unused

        length_bytes = io_in.read(2)
        length = int.from_bytes(length_bytes, "little") + 2
        if length > 2000:
            print("strange length:", length)
            continue

        sp_data = io_in.read(length)
        if len(sp_data) != length:
            print(f"incomplete packet, expected len: {length}, got: {len(sp_data)}")
            break

        (sp_header_crc, ) = struct.unpack(">H", sp_data[0:2])

        header_bytes = b'#' + preamble + length_bytes
        header_crc_sum = crc_fun(header_bytes)
        if header_crc_sum != sp_header_crc:
            print("RX header crc err, header bytes:", header_bytes,
                  header_crc_sum, sp_header_crc)

        sp_command_class = sp_data[2:3][0]
        sp_command = sp_data[3:4][0]
        sp_payload = sp_data[4:-2]

        crc = crc_fun(sp_data[2:])

        if crc != 0:
            print("TX Payload crc error!, crc:", hex(crc), ", data:",
                  binascii.hexlify(sp_data))
            # continue

        # print("\tsp_command_class:", hex(sp_command_class), ", ascii:", chr(sp_command_class))
        # print("\tsp_command:", hex(sp_command))
        # print("\tsp_payload len:", len(sp_payload))
        # print("\tsp_payload: 0x", binascii.hexlify(sp_payload))

        yield ((sp_command_class, sp_command, sp_payload))


def parse_serial_protocol_file(path):
    with open(path, 'rb') as f:
        yield from rtb_serial_protocol_parse(f)


if __name__ == "__main__":
    data = rtb_serial_protocol_encode('T', 'B', 'c', None)
    print("encoded:", data)

    io = io.BytesIO(data)
    for msg in rtb_serial_protocol_parse(io):
        print("msg:", msg)

    # for frame in parse_serial_protocol_file(sys.argv[1]):
    #     print("PARSE", frame)
