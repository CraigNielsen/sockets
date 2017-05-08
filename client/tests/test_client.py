import unittest
from unittest import TestCase
from ..client import parse_message, split_multiple_messages, SickClient

# These tests are all the same.
class TestSickClient(TestCase):
    def setUp(self):
        self.many_messages="^41822|30|50^^44104|30|50^^44104|30|50^^44104|30|50^^66074|30|50^^36259|30|50^^36259|30|50^"

    def test_split_many_messages(self):
        messages = split_multiple_messages(self.many_messages)
        self.assertEqual(messages[0], "41822|30|50")
        self.assertEqual(messages[1], "44104|30|50")
        self.assertEqual(messages[2], "44104|30|50")

    def test_parse_single_message(self):
        messages = split_multiple_messages(self.many_messages)
        message = parse_message(messages[0])
        expecting = {'slabel': 41822, 'height': 30, 'width': 50}
        self.assertEqual(message, expecting)

    # def test_server_test(self):
        #create client
#create test_server
#set server response to expect
#set server load
#handle mutliple clients
#ensure mocked function not called many times(after check for key in memcache)
    # def test_client_doesnt_make_multiple_calls_for_same_slable(self):
    def test_sick_client_setup(self):
        sc = SickClient()
        sc.connect()
        import pdb
        pdb.set_trace()
        sc.start_comms()

