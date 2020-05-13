import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT
import node_ring as node
import lru_cache as LRU
import bloom_filter

BUFFER_SIZE = 1024
cache = LRU.Cache(5)
bloomfilter = bloom_filter.BloomFilter(20, 0.05)

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

def process(udp_clients):
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        fix_me_server_id = ring.get_node(key)["port"]
        #PUT FUNCTION FOR ASSIGNMENT 3
        put(key, data_bytes) #PUT FUNCTION FOR ASSIGNMENT 3
        #PUT FUNCTION FOR ASSIGNMENT 3
        response = udp_clients[fix_me_server_id].send(data_bytes)
        hash_codes.add(response)
        print(response)

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")

    # GET all users.
    for hc in hash_codes:

        data_bytes, key = serialize_GET(hc)
        fix_me_server_id = ring.get_node(hc.decode())["port"]
        if get(key):
            response = udp_clients[fix_me_server_id].send(data_bytes)
            print(response)
        else:
            print("Key does not exist in server!")


#I implemented this in a way that I just put it back in the loop of PARTS I and PUT loop.
@LRU.lru_cache(5)
def get(key):
    global bloomfilter
    if bloomfilter.is_member(key):
        return True
    else:
        return False

def put(key, value):
    global bloomfilter
    bloomfilter.add(key)

def delete(key):
    global bloomfilter
    if bloomfilter.is_member(key):
        return udp_client.delete(key)
    else:
        return None



if __name__ == "__main__":

    clients = {}
    for server in NODES:
        clients[server["port"]] = UDPClient(server['host'], server['port'])
    ring = node.NodeRing(nodes = NODES)
    process(clients)
