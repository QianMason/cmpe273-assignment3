import sys
import socket
import pickle

from server_config import NODES
from pickle_hash import deserialize, hash_code_hex

BUFFER_SIZE = 1024

class MyDict(dict):
    def __init__(self):
        self = dict()

    def put(self, key, value):
        self[key] = value
        return key

class UDPServer():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.db = MyDict()


    def extract_request(self, data_bytes):
        request = deserialize(data_bytes)
        operation = request['operation']
        key = request['id']
        payload = None
        if 'payload' in request:
            payload = request['payload']
        print(f'operation={operation}\nid={key}\npayload={payload}')
        response = self.handle_operation(operation, key, payload)
        return response


    def handle_operation(self, operation, key, value):
        if operation == 'GET':
            # TODO: PART I - implement GET retrieval from self.db.xxxxx
            #return 'FIX_ME'.encode()
            return pickle.dumps(self.db[key.decode()])
        elif operation == 'PUT':
            print(self.db)
            return self.db.put(key, value)

        else:
            print(f'Error: Invalid operation={operation}')
            return 'Not supported operation={}'.format(operation)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))

        while True:
            data, ip = s.recvfrom(BUFFER_SIZE)
            print("{}:size={}".format(ip, len(data)))
            response = self.extract_request(data)
            # reply back to the client
            if isinstance(response, str):
                response = response.encode()

            s.sendto(response, ip)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Missing server index as argument. Usage: python3 cache_client.py [0-{}]'.format(len(NODES)-1))
        sys.exit(2)

    node_index = int(sys.argv[1])
    node = NODES[node_index]
    udpServer = UDPServer(node['host'], node['port'])
    print('Cache Server[{}] started at {}:{}'.format(node_index, node['host'], node['port']))
    udpServer.run()
