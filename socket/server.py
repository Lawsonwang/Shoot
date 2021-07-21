import socket
import threading

HOST = '192.168.3.110'
PORT = 233
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.bind((HOST, PORT))  # 套接字绑定的IP与端口
s.listen(10)  # 开始TCP监听

clients = set()


def sendall(msg):
    for each in clients:
        try:
            each.send(msg.encode('utf-8'))
        except:
            pass


def recv(sock):
    try:
        while True:
            data = sock.recv(1024).decode('utf-8')
            sendall(data)
            if data == '.quit':
                break
            else:
                print(data)
    except ConnectionResetError:
        pass
    finally:
        clients.remove(sock)
        sock.close()


while True:
    conn, addr = s.accept()
    clients.add(conn)
    t = threading.Thread(target=recv, args=(conn,))
    t.start()

# so, addr = s.accept()
# running = True
#
#
# def recv(sock):
#     global running
#     while running:
#         rec = sock.recv(1024).decode('utf-8')
#         if rec == 'exit':
#             continue
#         print(rec)


# recv(so)

# threading.Thread(target=recv, args=(so,)).start()

# while True:
#     send = input("Please input:")
#     if send == 'exit':
#         running = False
#         break
#     so.send(send.encode('utf-8'))
