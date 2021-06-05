import socket
HOST = '192.168.3.110'
PORT = 233
while True:
    cmd = input("Please input:")        # 与人交互，输入命令
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # 定义socket类型，网络通信，TCP
    s.connect((HOST, PORT))        # 要连接的IP与端口
    s.send(cmd.encode('utf-8'))       # 把命令发送给对端
    data = s.recv(1024)      # 把接收的数据定义为变量
    print(data.decode('utf-8'))          # 输出变量
    s.close()
