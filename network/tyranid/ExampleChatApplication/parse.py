# This is based off of code from
# https://jhalon.github.io/reverse-engineering-protocols/

import io
import os
from struct import unpack
import sys

MSG_TYPES = {
    0x0: "syn",
    0x1: "ack",
    0x2: "bye",
    0x3: "msg",
}


# Read a fixed number of bytes, dictated by "length".
def read_bytes(f, length):
    bytes = f.read(length)
    if len(bytes) != length:
        raise Exception("Not enough bytes in stream: %d vs %d" %
                        (len(bytes), length))
    return bytes


# Unpack a 4 byte integer in network byte order.
def read_int(f):
    return unpack("!i", read_bytes(f, 4))[0]


# Read a single byte.
def read_byte(f):
    return ord(read_bytes(f, 1))


# Read a string from data.
def read_string(f):
    length = read_byte(f)
    string = read_bytes(f, length)
    return string


# Extract multiple strings from data.
def extract_strings(data):
    parts = []
    f = io.BytesIO(data)
    while f.tell() < len(data):
        part = read_string(f)
        if part:
            parts.append(part)
    return parts


class Packet(object):
    def __init__(self, f) -> None:
        self.length = read_int(f)
        self.checksum = read_int(f)
        self.msg_type = read_byte(f)
        self.data_bytes = read_bytes(f, self.length - 1)
        self.data_parts = extract_strings(self.data_bytes)

    def __str__(self) -> str:
        string = f"{self.length: > 3} | {self.checksum: > 5} | "
        string += MSG_TYPES[self.msg_type]
        if self.data_parts:
            string += " | " + " | ".join([str(x) for x in self.data_parts])
        return string


if __name__ == "__main__":
    filename = sys.argv[1]
    file_size = os.path.getsize(filename)

    with open(filename, "rb") as f:
        conn = read_bytes(f, 4)
        if conn == b"BINX":
            # The first four bytes indicate a connection.
            print("Connection: %s" % conn)
        else:
            # The first four bytes do not indicate a connection. Reset the file
            # reader.
            f.seek(0)

        # Keep reading until file is empty.
        while f.tell() < file_size:
            print(str(Packet(f)))
