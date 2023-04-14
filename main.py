from pygame import *
init()
mixer.init()
font.init()

info = display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h

window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load("images/breakdown.png"), (WIDTH, HEIGHT))

mixer.music.load("sounds/is-that-a-jojo-reference-By-Tuna.ogg")
mixer.music.set_volume(0.2)
mixer.music.play()

kick = mixer.Sound("sounds/kick.ogg")
money = mixer.Sound("sounds/money.ogg")

clock = time.Clock()
FPS = 60

font1 = font.Font(None, HEIGHT // 8)

win_text = font1.render("YOU WIN!", True, (255, 240, 100))
lose_text = font1.render("YOU LOSE!", True, (255, 50, 50))

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (100, 140))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y <= HEIGHT - HEIGHT // 8:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= WIDTH - HEIGHT // 8:
            self.rect.x += self.speed
        if keys_pressed[K_g]:
            self.speed += 1     # не знаю нашо воно тут

class Enemy(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed)
        self.direction = "right"

    def update(self):
        if self.rect.x >= WIDTH - HEIGHT // 8:
            self.direction = "left"
        if self.rect.x <= WIDTH - WIDTH // 2.3:
            self.direction = "right"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

player = Player("images/higashikata.png", WIDTH // 10, HEIGHT - HEIGHT // 3, 10)
treasure = GameSprite("images/treasure.png", WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 1.2, 10)
monster = Enemy("images/SheerHeartAttack.jpg", WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 1.9, 10)
mem = GameSprite("images/kira_meme.jpg", WIDTH // 3.7, HEIGHT - HEIGHT // 2, 10)
mem.image = transform.scale(mem.image, (mem.rect.width * 3, mem.rect.height * 1.5))

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.color = (190, 210, 130)
        self.image = Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

walls = []

wall_width = HEIGHT // 80

wall_top = Wall(WIDTH // 20, HEIGHT // 15, WIDTH // 1.1, wall_width)
walls.append(wall_top)
wall_bot = Wall(WIDTH // 20, HEIGHT - HEIGHT // 15, WIDTH // 1.1, wall_width)
walls.append(wall_bot)

wall_1 = Wall(WIDTH // 4.5, HEIGHT // 3, wall_width, HEIGHT // 1.7)
walls.append(wall_1)

wall_2 = Wall(WIDTH // 4.4, HEIGHT // 3, WIDTH // 3.3, wall_width)
walls.append(wall_2)

wall_3 = Wall(WIDTH // 1.9, HEIGHT // 3, wall_width, HEIGHT // 1.7)
walls.append(wall_3)

wall_4 = Wall(WIDTH // 4.5, HEIGHT // 3, wall_width, HEIGHT // 2.5)
walls.append(wall_4)

wall_5 = Wall(WIDTH // 1.4, HEIGHT // 12, wall_width, HEIGHT // 1.7)
walls.append(wall_5)

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_r:
                finish = False
                player.rect.x = WIDTH // 10
                player.rect.y = HEIGHT - HEIGHT // 5

    if not finish:
        window.blit(background, (0, 0))

        player.update()
        monster.update()

        for wall in walls:
            wall.draw_wall()

            if sprite.collide_rect(player, wall):
                kick.play()
                window.blit(lose_text, (WIDTH // 2.5, HEIGHT // 2.5))
                finish = True

        if sprite.collide_rect(player, monster):
            kick.play()
            window.blit(lose_text, (WIDTH // 2.5, HEIGHT // 2.5))
            finish = True

        if sprite.collide_rect(player, treasure):
            money.play()
            window.blit(win_text, (WIDTH // 2.5, HEIGHT // 2.5))
            finish = True

        player.reset()
        monster.reset()
        treasure.reset()
        mem.reset()

    display.update()
    clock.tick(FPS)