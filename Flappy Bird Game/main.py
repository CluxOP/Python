import pygame, sys, random

# Prerequisites
pygame.init()
screen = pygame.display.set_mode((288,512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
user_score = 0
user_scores = []
user_high_score = 0

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_image_1 = pygame.image.load(r"sprites\bluebird-downflap.png").convert_alpha()
        self.player_image_2 = pygame.image.load(r"sprites\bluebird-midflap.png").convert_alpha()
        self.player_image_3 = pygame.image.load(r"sprites\bluebird-upflap.png").convert_alpha()
        self.player_animation_list = [self.player_image_1, self.player_image_2, self.player_image_3]
        self.animation_index = 0

        self.image = self.player_animation_list[self.animation_index]
        self.rect = self.image.get_rect(center = (50,256))
        
        self.gravity = 0
        self.key_delay = False

    def apply_gravity(self):
        self.gravity += 0.2
        self.rect.y += self.gravity

    def player_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.key_delay == False:
            self.gravity -= 10
            self.key_delay = True

    def player_animation(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.player_animation_list):
            self.animation_index = 0
        self.image = self.player_animation_list[int(self.animation_index)]
            
    def update(self):
        self.apply_gravity()
        self.player_input()
        self.player_animation()

class Objects(pygame.sprite.Sprite):
    def __init__(self, pipe):
        super().__init__()
        self.image = pygame.image.load(r"sprites\pipe-green.png").convert_alpha()

        if pipe == "top_pipe":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft = (350, random.randint(200, 412)))
        else:
            self.rect = self.image.get_rect(topleft = (350, random.randint(200,375)))

    def update(self):
        self.rect.x -= 1
        self.kill_objects()

    def kill_objects(self):
        if self.rect.x < -100:
            self.kill()

def collison():
    if pygame.sprite.spritecollide(player.sprite, object_group, False):
        player.sprite.gravity += 1
        return False
    elif player.sprite.rect.y <= 0 or player.sprite.rect.y >= 512:
        return False
    return True

def count_score():
    x_cord = 120
    y_cord = 25
    for i in str(user_score).zfill(2):
        screen.blit(font_image[i], (x_cord,y_cord))
        x_cord += 25

def bg_animation():
    screen.blit(bg_surf, bg_rect_1)
    screen.blit(bg_surf, bg_rect_2)
    screen.blit(bg_surf, bg_rect_3)

    bg_rect_1.x -= 2
    bg_rect_2.x -= 2
    bg_rect_3.x -= 2

    if bg_rect_1.x < -288:
        bg_rect_1.x = 576
    elif bg_rect_2.x < -288:
        bg_rect_2.x = 576
    elif bg_rect_3.x < -288:
        bg_rect_3.x = 576

# Import Images
bg_surf = pygame.image.load(r"sprites\background-day.png").convert()
bg_rect_1 = bg_surf.get_rect(topleft=(0,0))
bg_rect_2 = bg_surf.get_rect(topleft=(288,0))
bg_rect_3 = bg_surf.get_rect(topleft=(576,0))

game_over_img = pygame.image.load(r"sprites\gameover.png").convert_alpha()
game_over_img_rect = game_over_img.get_rect(center=(144,180))

# Font
font_image = {"0": pygame.image.load(r"sprites\0.png").convert_alpha(),
              "1": pygame.image.load(r"sprites\1.png").convert_alpha(),
              "2": pygame.image.load(r"sprites\2.png").convert_alpha(),
              "3": pygame.image.load(r"sprites\3.png").convert_alpha(),
              "4": pygame.image.load(r"sprites\4.png").convert_alpha(),
              "5": pygame.image.load(r"sprites\5.png").convert_alpha(),
              "6": pygame.image.load(r"sprites\6.png").convert_alpha(),
              "7": pygame.image.load(r"sprites\7.png").convert_alpha(),
              "8": pygame.image.load(r"sprites\8.png").convert_alpha(),
              "9": pygame.image.load(r"sprites\9.png").convert_alpha()}
font = pygame.font.Font(r"sprites\flappy-font.ttf", 24)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

object_group = pygame.sprite.Group()

# Timers
key_interval = pygame.USEREVENT + 1
pygame.time.set_timer(key_interval, 700)

object_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(object_spawn, 3500)

score = pygame.USEREVENT + 3
pygame.time.set_timer(score, 1000)

game_active = False

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == key_interval and player.sprite.key_delay == True:
                player.sprite.key_delay = False
            if event.type == object_spawn:
                object_group.add(Objects(random.choice(["top_pipe","bottom_pipe"])))
            if event.type == score:
                user_score += 1 

    if game_active:
        bg_animation()
        player.draw(screen)
        player.update()

        object_group.draw(screen)
        object_group.update()

        count_score()
        game_active = collison()
    else:
        screen.blit(bg_surf, (0,0))
        player.draw(screen)
        object_group.draw(screen)
        if user_score not in user_scores: user_scores.append(user_score)
        
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            object_group.empty()
            player.sprite.rect.y = 256
            user_score = 0
            player.sprite.gravity = 0
            game_active = True
            player.sprite.gravity -= 5

        if user_score == 0:
            screen.blit(pygame.font.Font.render(font, "Press Space to start", False, "white"), (10,475))
            screen.blit(pygame.font.Font.render(font, f"Highest Score: {user_high_score}", False, "yellow"), (45,10))
        elif user_score != 0:
            user_high_score = max(user_scores)
            screen.blit(game_over_img, game_over_img_rect)
            screen.blit(pygame.font.Font.render(font, f"Your Score: {user_score}", False, "yellow"), (60,220))
            screen.blit(pygame.font.Font.render(font, f"Highest Score: {user_high_score}", False, "yellow"), (45,250))
            screen.blit(pygame.font.Font.render(font, f"Space to Restart", False, "white"), (38,475))
            player.sprite.gravity += 100

    pygame.display.update()
    clock.tick(60)