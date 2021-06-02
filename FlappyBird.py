import pygame
import sys
import random
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 530))
    screen.blit(floor_surface, (floor_x_pos + 400, 530))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(730, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos - 520))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 400:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 530:
        death_sound.play()
        return False
    return True


def rotateBird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rectangle.centery))
    return new_bird, new_bird_rect


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f"Score: {str(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f"Score: {str(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"HighScore: {str(int(highScore))}", True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(150, 60))
        screen.blit(high_score_surface, high_score_rect)


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
# Game Variables
window_width = 400
window_height = 600
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
highScore = 0

screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
game_font = pygame.font.Font(resource_path('Assets/fonts/04B_19.TTF'), 40)


bg_surface = pygame.image.load(resource_path('assets/images/background-night.png')).convert()
bg_surface = pygame.transform.scale(bg_surface, (400, 600))

floor_surface = pygame.image.load(resource_path('assets/images/base.png')).convert()
floor_surface = pygame.transform.scale(floor_surface, (400, 100))
floor_x_pos = 0

bird_downflap = pygame.image.load(resource_path('assets/images/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.image.load(resource_path('assets/images/yellowbird-midflap.png')).convert_alpha()
bird_upflap = pygame.image.load(resource_path('assets/images/redbird-upflap.png')).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center=(100, 300))
# bird_surface = pygame.image.load('./assets/images/bluebird-midflap.png').convert_alpha()
# bird_rectangle = bird_surface.get_rect(center=(100, 300))

pipe_surface = pygame.image.load(resource_path('assets/images/pipe-red.png'))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # Th
# is event is not triggered by user keyboard actions
pygame.time.set_timer(SPAWNPIPE, 1200)  # 1.2 sec
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
pipe_height = [230, 250, 270, 300, 350, 400, 450]
game_over_surface = pygame.image.load('./assets/images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(200, 300))
flap_sound = pygame.mixer.Sound(resource_path('assets/audio/wing.wav'))
death_sound = pygame.mixer.Sound(resource_path('assets/audio/hit.wav'))
score_sound = pygame.mixer.Sound(resource_path('assets/audio/point.wav'))

# game loop
while True:
    clock.tick(80)
    # Event loop
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rectangle.center = (100, 300)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3
            bird_surface, bird_rect = bird_animation()

    # Background
    screen.blit(bg_surface, (0, 0))

    if game_active == True:
        # Bird
        bird_movement += gravity
        bird_rectangle.centery += bird_movement
        rotated_bird = rotateBird(bird_surface)
        screen.blit(rotated_bird, bird_rectangle)
        game_active = check_collision(pipe_list)

        # Pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        highScore = update_score(score, highScore)
        score_display('game_over')

    # Floor
    screen.blit(floor_surface, (floor_x_pos, 530))
    floor_x_pos -= 1
    draw_floor()
    if (floor_x_pos <= -400):
        floor_x_pos = 0

    # Display Screen Update
    pygame.display.update()
