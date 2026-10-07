import socket
import ssl
import threading
import time
import os
import binascii
from message_encryption import MessageEncryption

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CA_CERT = os.path.join(BASE_DIR, 'certs', 'ca', 'ca.crt')
CLIENT_CERT = os.path.join(BASE_DIR, 'certs', 'client', 'client.crt')
CLIENT_KEY = os.path.join(BASE_DIR, 'certs', 'client', 'client.key')

def test_full_communication():
    # Connect client 1 (khanh)
    key1 = os.urandom(32)
    me1 = MessageEncryption(key1)
    
    ctx1 = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
    ctx1.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    ctx1.check_hostname = False
    ctx1.verify_mode = ssl.CERT_REQUIRED
    
    s1 = socket.socket()
    ssl1 = ctx1.wrap_socket(s1, server_hostname='127.0.0.1')
    ssl1.connect(('127.0.0.1', 8443))
    ssl1.send(f"khanh:{binascii.hexlify(key1).decode()}".encode())
    
    # Connect client 2 (bob)
    key2 = os.urandom(32)
    me2 = MessageEncryption(key2)
    
    ctx2 = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
    ctx2.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    ctx2.check_hostname = False
    ctx2.verify_mode = ssl.CERT_REQUIRED
    
    s2 = socket.socket()
    ssl2 = ctx2.wrap_socket(s2, server_hostname='127.0.0.1')
    ssl2.connect(('127.0.0.1', 8443))
    ssl2.send(f"bob:{binascii.hexlify(key2).decode()}".encode())
    
    time.sleep(0.5)
    
    # Client 1 sends a message
    secret_text = "Xin chao buoi 3 tu Pham Duy Khanh!"
    enc_msg = me1.encrypt(secret_text)
    ssl1.send(enc_msg)
    
    # Client 2 should receive it
    received_raw = ssl2.recv(4096)
    decrypted = me2.decrypt(received_raw)
    print(f"Client Bob received: {decrypted}")
    assert "[khanh]: Xin chao buoi 3 tu Pham Duy Khanh!" in decrypted
    print("Integration communication test PASSED!")
    
    ssl1.close()
    ssl2.close()

if __name__ == '__main__':
    test_full_communication()
