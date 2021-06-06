import pygame
import socket
import json

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shoot!")

HOST = '192.168.3.110'
PORT = 233

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.bind((HOST, PORT))  # 套接字绑定的IP与端口
s.listen(10)  # 开始TCP监听
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
    print('Connected by', addr)  # 输出客户端的IP地址
    try:
        data = conn.recv(1024).decode('utf-8')
        data = json.loads(data)
        # print(data)
        # conn.send(data)
        screen.fill((0, 0, 0))
        for each in data['players']:
            img = 'player' + str(each['player']) + '.png'
            image = pygame.image.load(img).convert_alpha()
            image = pygame.transform.rotate(image, each['angle'])
            screen.blit(image, (each['rect'][0], each['rect'][1]))
        for each in data['bullets']:
            img = 'bullet.png'
            image = pygame.image.load(img).convert_alpha()
            screen.blit(image, (each['rect'][0], each['rect'][1]))
        # image0 = pygame.image.load(image).convert_alpha()
    except ConnectionResetError as e:
        pass
        # print('关闭了正在占线的链接！')
    pygame.display.flip()
    conn.close()  # 关闭连接

pygame.quit()
