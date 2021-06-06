import socket
import json

HOST = '192.168.3.110'
PORT = 233
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.bind((HOST, PORT))  # 套接字绑定的IP与端口
s.listen(10)  # 开始TCP监听
while 1:
    conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
    print('Connected by', addr)  # 输出客户端的IP地址
    try:
        data = conn.recv(1024).decode('utf-8')
        data = json.loads(data)
        print(data)
        # conn.send(data)
    except ConnectionResetError as e:
        pass
        # print('关闭了正在占线的链接！')
    conn.close()  # 关闭连接
