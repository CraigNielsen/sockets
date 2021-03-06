# from testing_config import messages as test_messages
from server import TestingTCPThreadedServer, RandomTCPThreadedServer
from ..testing.helper import generate_messages

if __name__ == "__main__":
    while True:
        port_num = 5005
        # port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    # print("running Random Threaded Server")
    # RandomTCPThreadedServer('', port_num).listen()
    print("running Testing Threaded Server")
    TestingTCPThreadedServer('',port_num, generate_messages(5000,6000), 100).listen()
