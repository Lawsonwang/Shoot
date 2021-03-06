import pygame
from math import *


class Player(pygame.sprite.Sprite):
    blood = 10

    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image0 = pygame.image.load(image).convert_alpha()
        self.image = self.image0
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.wid = self.rect.width
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4
        self.angle = 0.0
        self.radius = 30 / 2
        self.blood = 10
        self.active = True

    def move(self, d):
        self.rect.top += d[0] * self.speed
        self.rect.left += d[1] * self.speed
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width

    def rotate(self, angle=0.0):
        self.image = pygame.transform.rotate(self.image0, angle)
        tmp = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = tmp
        self.angle = angle


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, owner):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        # self.image = pygame.image.load(image).convert_alpha()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.radius = 10 / 2
        self.owner = owner

    def move(self):
        self.rect.top += self.speed[0]
        self.rect.left += self.speed[1]
        if self.rect.top <= 0:
            return True
        if self.rect.bottom >= height:
            return True
        if self.rect.left <= 0:
            return True
        if self.rect.right >= width:
            return True
        return False


def main():
    global width, height, bullet_img
    pygame.init()
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Shoot!")
    clock = pygame.time.Clock()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    bullet_speed = 10
    player1 = Player("player1.png", (100, 100))
    player2 = Player("player2.png", (width // 2, height // 2))
    bullet_img = pygame.image.load('bullet.png').convert_alpha()
    bullet_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group((player1, player2))
    running = True
    cnt = 1
    cnt1 = cnt2 = 0
    bullet_time = 20
    while running:
        if player1.active:
            pos = pygame.mouse.get_pos()
            alpha = atan2((player1.rect.centery - pos[1]), (pos[0] - player1.rect.centerx))
            player1.rotate(alpha / pi * 180 - 90)

        # ??????
        if player1.active and player2.active:
            alpha = atan2((player2.rect.centery - player1.rect.centery), (player1.rect.centerx - player2.rect.centerx))
            player2.rotate(alpha / pi * 180 - 90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player1.active and cnt1 >= bullet_time:
                        cnt1 = 0
                        bullet_group.add(Bullet('bullet.png', player1.rect.center,
                                            (-cos(player1.angle / 180 * pi) * bullet_speed,
                                             -sin(player1.angle / 180 * pi) * bullet_speed), player1))
                elif event.button == 3:
                    for each in player_group.spritedict:
                        print(each.__dict__)
                    print(bullet_group.spritedict)
                    print()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    if player2.active and cnt2 >= 20:
                        cnt2 = 0
                        bullet_group.add(Bullet('bullet.png', player2.rect.center,
                                            (-cos(player2.angle / 180 * pi) * bullet_speed,
                                             -sin(player2.angle / 180 * pi) * bullet_speed), player2))

        # ??????
        # cnt = (cnt + 1) % 20
        # if cnt == 0 and player1.active and player2.active:
        #     bullet_group.add(Bullet('bullet.png', player2.rect.center,
        #                             (-cos(player2.angle / 180 * pi) * bullet_speed,
        #                              -sin(player2.angle / 180 * pi) * bullet_speed), player2))

        cnt1 += 1
        if cnt1 >= bullet_time + 20:
            cnt1 -= 10
        cnt2 += 1
        if cnt2 >= bullet_time + 20:
            cnt2 -= 10

        screen.fill(BLACK)

        if player1.active:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                player1.move((-1, 0))
            if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                player1.move((1, 0))
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                player1.move((0, -1))
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                player1.move((0, 1))

        if player2.active:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_i] or key_pressed[pygame.K_UP]:
                player2.move((-1, 0))
            if key_pressed[pygame.K_k] or key_pressed[pygame.K_DOWN]:
                player2.move((1, 0))
            if key_pressed[pygame.K_j] or key_pressed[pygame.K_LEFT]:
                player2.move((0, -1))
            if key_pressed[pygame.K_l] or key_pressed[pygame.K_RIGHT]:
                player2.move((0, 1))

        for each in bullet_group:
            if each.move():
                bullet_group.remove(each)
            screen.blit(each.image, each.rect)
            player_group.remove(each.owner)
            pls = pygame.sprite.spritecollide(each, player_group, False, pygame.sprite.collide_circle)
            if pls:
                bullet_group.remove(each)
                for pl2 in pls:
                    pl2.blood -= 1
                    if pl2.blood <= 0:
                        print('Kill!')
                        player_group.remove(pl2)
                        pl2.active = False
            if each.owner.active:
                player_group.add(each.owner)

        for each in player_group:
            if each.active:
                remain = each.blood / Player.blood
                if remain > 0.5:
                    color = GREEN
                elif remain > 0.2:
                    color = YELLOW
                else:
                    color = RED
                pygame.draw.line(screen, GRAY, (each.rect.left + each.wid * remain, each.rect.bottom - 5),
                                 (each.rect.left + each.wid - 1, each.rect.bottom - 5), 2)
                pygame.draw.line(screen, color, (each.rect.left, each.rect.bottom - 5),
                                 (each.rect.left + each.wid * remain, each.rect.bottom - 5), 2)
                screen.blit(each.image, each.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
