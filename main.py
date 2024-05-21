from __future__ import division
import pygame
import random
from os import path

icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')


WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BamBoom!!!")
clock = pygame.time.Clock()
###############################

font_name = pygame.font.match_font('bold')

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.wav"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir, "main.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)

    screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:
            draw_text(screen, "Нажмите [ENTER] чтобы начать", 35, WIDTH/2, HEIGHT/2, color=(128, 0, 0))
            draw_text(screen, "или [Q] чтобы выйти =(", 30, WIDTH/2, (HEIGHT/2)+40, color=(139, 69, 19))
            pygame.display.update()


    ready = pygame.mixer.Sound(path.join(sound_folder,'nachalo-igryi.wav'))
    ready.set_volume(0.2)
    ready.play()
    screen.fill(color=(139, 69, 19))
    draw_text(screen, "НАЧИНАЕМ!", 40, WIDTH/2, HEIGHT/2, color=(255, 160, 122))
    pygame.display.update()


def draw_text(surf, text, size, x, y, color=WHITE):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_heart_bar(surf, x, y, pct):

    pct = max(pct, 0)

    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 80:
        color = [0,255,209]
    elif pct > 60:
        color = [0,255,55]
    elif pct > 40:
        color = [239,255,0]
    else:
        color = [255,0,0]
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(player_img, (90, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.heart = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):

        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()


        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0



        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5


        if keystate[pygame.K_SPACE]:
            self.shoot()


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx

    def shoot(self):

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            """ MOAR POWAH """
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(ball_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)


        self.speedx = random.randrange(-3, 3)


        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50:
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy


        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['heart', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.speedy = 2

    def update(self):

        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):

        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()



background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()


player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'arrow.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()

ball_images = []
ball_list = [
    'ball_big1.png',
    'ball_big2.png',
    'ball_med 2.png',
    'ball_med1.png',
    'ball_small1.png',
    'ball_small2.png',
    'ball_tiny.png'
]

for image in ball_list:
    ball_images.append(pygame.image.load(path.join(img_dir, image)).convert())


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)

    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


powerup_images = {}
powerup_images['heart'] = pygame.image.load(path.join(img_dir, 'heart.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'mana.png')).convert()


###################################################


###################################################

shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'ognen_shar.wav'))
shooting_sound.set_volume(0.4)
missile_sound.set_volume(0.4)
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
    expl_sounds[-1].set_volume(0.1)

pygame.mixer.music.set_volume(0.2)

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'inecraft_death.wav'))
###################################################

#############################

running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)


        pygame.mixer.music.stop()

        pygame.mixer.music.load(path.join(sound_folder, 'main-menu-2.wav'))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        menu_display = False


        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)


        mobs = pygame.sprite.Group()
        for i in range(8):

            newmob()


        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()


        score = 0


    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    all_sprites.update()



    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()

        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()


    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.heart -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.heart <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)

            player.hide()
            player.lives -= 1
            player.heart = 100


    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'heart':
            player.heart += random.randrange(10, 30)
            if player.heart >= 100:
                player.heart = 100
        if hit.type == 'gun':
            player.powerup()


    if player.lives == 0 and not death_explosion.alive():
        while True:
            screen.fill(color=(139, 69, 19))
            draw_text(screen, "Игра окончена =(", 48, WIDTH / 2, HEIGHT / 4, color=(255, 160, 122))
            draw_text(screen, "Результат: " + str(score), 35, WIDTH / 2, HEIGHT / 2, color=(255, 160, 122))
            draw_text(screen, 'Нажмите "Q" чтобы выйти из игры', 30, WIDTH / 2, HEIGHT * 3 / 4, color=(255, 160, 122))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()






    screen.fill(BLACK)

    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_heart_bar(screen, 5, 5, player.heart)


    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)


    pygame.display.flip()

pygame.quit()
