#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting')

   msg = c.recv(1024)
   print msg
   
   #correct GET message, sampled from when i call index on my app.py
   if msg == "GET / HTTP/1.1":
   		new_msg = "GET / HTTP/1.1\r\n\r\n"
   		print "in"
   		#hostname = "http://host-21-166.miellan.clients.pavlovmedia.com/"
   		#port = 8617
   		hostname = "www.google.com"
   		port = 80
   		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   		remote_ip = socket.gethostbyname(hostname)
   		sock.connect((remote_ip, port))
   		sock.sendall(new_msg)
   		reply = sock.recv(4096)
 
   		print reply
   		c.send(reply)

   time.sleep(2)
   c.send("good bye.")
   c.close()