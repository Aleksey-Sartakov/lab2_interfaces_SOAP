import socket
import xml.etree.ElementTree as ET
import os


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostbyname(socket.gethostname())
        self.client.connect((self.host_name, 7000))


        """
        <?xml version="1.0"?>
        <soap:Envelope
            xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
            soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">
        <soap:Body> 
            <{function}>
                <Item>{data}</m:Item>
            </{function}>
        </soap:Body>
        </soap:Envelope>
        """

    def connect(self):
        try:
            f = open("client.xml", "wb")
            file_size = self.client.recv(1024)
            received_bytes = 0
            while bytes(received_bytes) < file_size:
                l = self.client.recv(1024)
                if l:
                    f.write(l)
                    received_bytes += len(l)

            print("in try")
            f.close()

        except Exception as e:
            print(f"Error: {str(e)}")
            exit()

        tree = ET.parse("client.xml")
        os.remove("./client.xml")
        root = tree.getroot()
        print(root[0][0].tag)
        msg = tree.find(".//Item").text

        if msg == "You are successfully connected!":
            print(msg)
            self.listen()
        else:
            exit()

    def sender(self, data):
        envelope = ET.Element("soap:Envelope")
        body = ET.SubElement(envelope, "soap:Body")
        if data == "disconnect":
            function = ET.SubElement(body, "Disconnect")
        else:
            function = ET.SubElement(body, "Void")
        item = ET.SubElement(function, "Item")

        envelope.set("xmlns:soap", "http://www.w3.org/2003/05/soap-envelope/")
        envelope.set("soap:encodingStyle", "http://www.w3.org/2003/05/soap-encoding")
        item.text = data

        tree = ET.ElementTree(envelope)
        tree.write("client.xml")

        file_size = os.path.getsize("client.xml")
        self.client.send(bytes(file_size))

        f = open("client.xml", "rb")
        while l := f.read(1024):
            self.client.send(l)

        f.close()
        os.remove("./client.xml")

        # while self.client.recv(1024).decode('utf-8') != "get":
        #     self.client.send(text.encode('utf-8'))

    def listen(self):
        is_work = True

        while is_work:
            request = input('Type some request: ')

            if request in valid_requests:
                self.sender(request)

                try:
                    f = open("client.xml", "wb")

                    file_size = self.client.recv(1024)
                    received_bytes = 0

                    while bytes(received_bytes) < file_size:
                        l = self.client.recv(1024)
                        if l:
                            f.write(l)
                            received_bytes += len(l)

                    f.close()
                except Exception as e:
                    is_work = False

                try:
                    tree = ET.parse("client.xml")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    exit()

                os.remove("./client.xml")
                root = tree.getroot()
                response = root[0][0].tag
                if response == "DisconnectResponse":
                    is_work = False
                    print(tree.find(".//Item").text)


valid_requests = ["disconnect"]


if __name__ == "__main__":
    client = Client()
    client.connect()
