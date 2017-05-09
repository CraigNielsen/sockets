from client import SickClient

if __name__ == "__main__":
    sc = SickClient()
    sc.connect()
    sc.start_comms()
