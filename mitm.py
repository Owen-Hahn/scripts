import socket
import re
import argparse
import ssl

context = ssl.create_default_context()

parser = argparse.ArgumentParser()
parser.add_argument('host',help='ip address to listen to', default='')
parser.add_argument('port',help='port to bind and listen on', default=80,type=int)
parser.add_argument('rhost',help='remote host to connect to')
parser.add_argument('rport',help='remote port to connect to', default=80,type=int)
args = parser.parse_args()
HOST = args.host
PORT = args.port
RHOST = args.rhost
RPORT = args.rport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while 1:
  s.listen(1)
  conn, addr = s.accept()
  rs = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),server_hostname=RHOST)
  rs.connect((RHOST, RPORT))
  while 1:
      try:
        data = conn.recv(4096,socket.MSG_DONTWAIT)
        data = re.sub('{}:{}'.format(HOST,PORT),RHOST,str(data))
        if not data:
          rs.close()
          break
        print(data)
        rs.sendall(data.encode('utf-8'))
      except BlockingIOError:
        raise 
      try:
        rdata = rs.recv(4096 )
        print(rdata)
        conn.sendall(rdata)
      except:
        raise 
  conn.close()
