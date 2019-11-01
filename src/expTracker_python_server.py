import socket
import sys

maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#소켓 생성
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 7777
        s = socket.socket()

        maya.connect(("127.0.0.1", 7777))
    except socket.error as msg:
        print("soket creation error: " + str(msg))

#바인딩
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()

#연결 수용
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established|"+"IP: "+address[0]+"| Port: "+str(address[1]))
    send_commands(conn)
    conn.close()

#명령
def send_commands(conn):
    while True:
        client_response = str(conn.recv(2048), "utf=8")
        print(client_response, end="")                     # 이건 그냥 값 확인하려고 넣은 것.
        maya.send(client_response.encode())
        

def main():
    
    socket_create()
    socket_bind()
    socket_accept()

main()
