import zlib
#@maggie 我们开了个tempchat.txt
#是txt！！！！

class Package:
    def __init__(self):
        pass

    def encode(self, content, trytozip=True, zip_level=6):
        if trytozip:
            zipped = zlib.compress(content, zip_level)
            self.raw = content
            self.zipped = zipped
        else:
            self.raw = content
            self.zipped = content
        shouldzip = self.raw.__sizeof__() > self.zipped.__sizeof__()
        if shouldzip:
            data = self.zipped
        else:
            data = self.raw
        self.zipped = shouldzip
        self.data = bytes([int(shouldzip)])+data

        return self.data

    def decode(self, content):
        cont = list(content)
        zipped = bool(cont[0])
        string = bytes(cont[1:])
        self.zipped = zipped
        if zipped:
            inside = zlib.decompress(string)
        else:
            inside = string
        self.raw = inside
        return inside


class Socket:
    def __init__(self, socket):
        self.socket = socket

    def recv(self, size):
        data = self.socket.recv(size)
        if not data:
            raise IOError("Socket closed.")
        temp = Package()
        return temp.decode(data)

    def send(self, data, ziplevel=6):
        temp = Package()
        zipped = temp.encode(data, ziplevel)
        return self.socket.send(zipped)

    @property
    def fileno(self):
        return self.socket.fileno
