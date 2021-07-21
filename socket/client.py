import socket
import threading

running = True


def send(sock):
    global running
    while True:
        data = input()
        sock.send(data.encode("utf-8"))
        if data == ".quit":
            running = False
            break


def recv(sock):
    global running
    while running:
        try:
            rec = sock.recv(1024).decode('utf-8')
            if rec == '.quit':
                continue
            print(rec)
        except:
            break


HOST = '192.168.3.110'
PORT = 233
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    t1 = threading.Thread(target=recv, args=(s,))
    t2 = threading.Thread(target=send, args=(s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
except:
    pass
finally:
    s.close()



# threading.Thread(target=recv, args=(s,)).start()
#
# while True:
#     send = input("Please input:")
#     if send == 'exit':
#         running = False
#         break
#     s.send(send.encode('utf-8'))
