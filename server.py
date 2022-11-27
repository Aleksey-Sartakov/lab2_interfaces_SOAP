import socket
import xml.etree.ElementTree as ET
import os


class Server:
    def __init__(self):
        print("Server created...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostbyname(socket.gethostname())
        self.server.bind((self.host_name, 7000))
        self.server.listen(1)

    def start_server(self):
        while True:
            user, addres = self.server.accept()
            self.listen(user)

    def sender(self, user, func):
        envelope = ET.Element("soap:Envelope")
        body = ET.SubElement(envelope, "soap:Body")

        if func == "Disconnect":
            function = ET.SubElement(body, "DisconnectResponse")
            item = ET.SubElement(function, "Item")
            item.text = "You are disconnected"

        elif func == "ConnectResponse":
            function = ET.SubElement(body, func)
            item = ET.SubElement(function, "Item")
            item.text = "You are successfully connected!"

        envelope.set("xmlns:soap", "http://www.w3.org/2003/05/soap-envelope/")
        envelope.set("soap:encodingStyle", "http://www.w3.org/2003/05/soap-encoding")

        tree = ET.ElementTree(envelope)
        tree.write("server.xml")

        f = open("server.xml", "rb")
        file_size = os.path.getsize("server.xml")
        user.send(bytes(file_size))

        while l := f.read(1024):
            user.send(l)

        f.close()
        os.remove("./server.xml")

    def listen(self, user):
        print("client is connected")
        self.sender(user, "ConnectResponse")

        is_work = True

        while is_work:
            try:
                f = open("server.xml", "wb")
                file_size = user.recv(1024)
                received_bytes = 0
                while bytes(received_bytes) < file_size:
                    l = user.recv(1024)
                    if l:
                        f.write(l)
                        received_bytes += len(l)

                f.close()
            except Exception as e:
                is_work = False

            try:
                tree = ET.parse("server.xml")
            except Exception as e:
                f.close()
                os.remove("./server.xml")
                print("client is disconnected")
                break

            os.remove("./server.xml")
            root = tree.getroot()
            function = root[0][0].tag

            if function == "Disconnect":
                self.sender(user, function)
                user.close()
                print("client is disconnected")
                is_work = False


if __name__ == "__main__":
    server = Server()
    server.start_server()
