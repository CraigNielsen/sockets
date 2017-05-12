import unittest
from unittest import TestCase
import time
import threading
from testing_config import messages
from mock import patch, Mock
from .. import client
from ..client import parse_message, split_multiple_messages, SickClient, CLOSE, PING, do_something
# from sockets.server.server import TestingTCPThreadedServer

# These tests are all the same.
def openServer():
    message='^345345|50|50^'
    t = TestingTCPThreadedServer('', 5005, message, 1)
    import pdb
    pdb.set_trace()
    t.listen()

def openClient():
    sc = SickClient()
    sc.connect()
    sc.start_comms()

class TestSickClient(TestCase):
    def setUp(self):
        self.many_messages="^41822|30|50^^44104|30|50^^44104|30|50^^44104|30|50^^66074|30|50^^36259|30|50^^36259|30|50^"
        self.many_messages_with_pings="^41822|30|50^^{}^^66074|30|50^^36259|30|50^^36259|30|50^".format(PING)
        self.many_messages_with_close="^41822|30|50^^{}^^66074|30|50^^36259|30|50^^36259|30|50^".format(CLOSE)

    def test_split_many_messages(self):
        messages = split_multiple_messages(self.many_messages)
        self.assertEqual(messages[0], "41822|30|50")
        self.assertEqual(messages[1], "44104|30|50")
        self.assertEqual(messages[2], "44104|30|50")

    def test_parse_single_message(self):
        messages = split_multiple_messages(self.many_messages)
        message = parse_message(messages[0])
        expecting = {'slabel': '41822', 'height': 30, 'width': 50}
        self.assertEqual(message, expecting)

    def test_parse_single_message_with_pings(self):
        messages = split_multiple_messages(self.many_messages_with_pings)
        message = parse_message(messages[1])
        expecting = PING
        self.assertEqual(message, expecting)

    def test_parse_single_message_with_close(self):
        messages = split_multiple_messages(self.many_messages_with_close)
        message = parse_message(messages[1])
        expecting = CLOSE
        self.assertEqual(message, expecting)

    # def test_server_test(self):
    #create client
    #create test_server
    #set server response to expect
    #set server load
    #handle mutliple clients
    #ensure mocked function not called many times(after check for key in memcache)
    # def test_client_doesnt_make_multiple_calls_for_same_slable(self):


    @patch(client.__name__ + '.do_something', return_value=True)
    def test_sick_client_setup(self, ds):
        # with patch.object(SickClient, 'act_on_message_types', wraps=sc.act_on_message_types) as fun:
            sc = SickClient()
            #mock message act on message type function
            # sc2 = SickClient()
            sc.connect()
            # sc2.connect()
            sc.start_comms()
            from mock import  call
            self.assertEquals(len(ds.mock_calls), 3)
            ds.assert_has_calls([
                call({'width': 50, 'slabel': '51259', 'height': 30}),
                call({'width': 50, 'slabel': '42337', 'height': 30}),
                call({'width': 50, 'slabel': '25907', 'height': 30}),
            ])


