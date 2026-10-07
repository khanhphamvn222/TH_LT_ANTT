import unittest
import os
import socket
import ssl
import threading
import time
import binascii

from message_encryption import MessageEncryption
from connection_manager import ConnectionManager
from room_manager import RoomManager

class TestSecureChatComponents(unittest.TestCase):
    def test_message_encryption(self):
        key = os.urandom(32)
        me = MessageEncryption(key)
        secret = "Hello Secure World! Xin chào An Toàn Thông Tin"
        encrypted = me.encrypt(secret)
        self.assertNotEqual(encrypted, secret.encode('utf-8'))
        decrypted = me.decrypt(encrypted)
        self.assertEqual(decrypted, secret)

    def test_connection_manager(self):
        cm = ConnectionManager()
        s1 = socket.socket()
        key1 = os.urandom(32)
        cm.add_client(s1, "alice", key1)
        self.assertEqual(cm.get_client(s1)['username'], "alice")
        cm.remove_client(s1)
        self.assertIsNone(cm.get_client(s1))
        s1.close()

    def test_room_manager(self):
        rm = RoomManager()
        s1 = socket.socket()
        rm.create_room("general")
        rm.join_room("general", s1)
        self.assertIn(s1, rm.rooms["general"])
        rm.leave_room("general", s1)
        self.assertNotIn(s1, rm.rooms["general"])
        s1.close()

if __name__ == '__main__':
    unittest.main()
