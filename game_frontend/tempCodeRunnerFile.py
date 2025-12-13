import pygame
import random
import sys
import requests
import csv
import os

def submit_score(name, score):
    url = "http://127.0.0.1:5000/submit"
    data = {"name": name, "score": score}
    try:
        response = requests.post(url, json=data)
        print("Score submitted:", response.json())
    except Exception as e:
        print("Failed to submit score:", e)

def fetch_leaderboard():
    url = "http://127.0.0.1:5000/leaderboard"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Failed to fetch leaderboard:", e)
        return []

def save_score_to_csv(name, score, filename="./Car_fun/scores.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Score"])
        writer.writerow([name, score])

def load_scores_from_csv(filename="./Car_fun/scores.csv"):
    scores = []
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) == 2:
                    scores.append({"name": row[0], "score": int(row[1])})
    return scores

pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Vehicle Car Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

fuel = 100
fuel_decrease_rate = 0.05
fuel_can_img = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/fuel.png"), (40, 40))
fuel_x, fuel_y = random.randint(50, WIDTH-50), -100
fuel_speed = 5

# Load assets
car_images = [
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_k.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_l.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_m.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_n.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_o.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_p.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/pla/car_q.png"), (150, 200))
]
selected_car_index = 0

road_images = [
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_2.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_3.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_4.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_5.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_6.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_7.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_8.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_9.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_10.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_11.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/rd/road_12.png"), (WIDTH, HEIGHT))
    ]
selected_road_index = 0

enemy_vehicles = [
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car1.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car2.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car3.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car4.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car5.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car6.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car7.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car8.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car9.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car10.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car11.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car12.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car13.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car14.png"), (150, 200)),
    pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/emy/car15.png"), (150, 200))
]
opening_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/opening_bg.jpg"), (WIDTH, HEIGHT))
gameresume_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/resume.png"), (WIDTH, HEIGHT))
gameover_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/over.png"), (WIDTH, HEIGHT))
name_input_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/input.png"), (WIDTH, HEIGHT))
instructions_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/ins.png"), (WIDTH, HEIGHT))
change_bg = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/change.jpg"), (WIDTH, HEIGHT))
heart_image = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/heart.png"), (50, 50))
fire_image = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/fire.png"), (60, 60))
coin_image = pygame.transform.scale(pygame.image.load("./Car_fun/game_frontend/file/oth/coin.png"), (45, 45))


# Load sounds
jump_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/jump.mp3")
collect_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/heart.mp3")
crash_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/over.mp3")
coin_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/coin.mp3")
fire_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/fire.wav")
fuel_sound = pygame.mixer.Sound("./Car_fun/game_frontend/sounds/s2/fuel.mp3")

bg_music_files = [
    "./Car_fun/game_frontend/sounds/s1/bg1.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg2.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg3.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg4.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg5.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg6.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg7.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg8.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg9.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg10.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg11.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg12.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg13.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg14.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg15.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg16.mp3",
    "./Car_fun/game_frontend/sounds/s1/bg17.mp3"
]

pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
current_music_index = 0

pygame.draw.rect(screen, (0,0,0), (10, 10, 200, 20))
pygame.draw.rect(screen, (255,255,0), (10, 10, int(fuel*2), 20))

screen.blit(fuel_can_img, (fuel_x, fuel_y))

def play_next_music():
    global current_music_index
    pygame.mixer.music.load(bg_music_files[current_music_index])
    pygame.mixer.music.set_volume(current_volume)
    pygame.mixer.music.play()
    current_music_index = (current_music_index + 1) % len(bg_music_files)

# Sound settings
current_volume = 1.0
pygame.mixer.music.set_volume(current_volume)
jump_sound.set_volume(current_volume)
collect_sound.set_volume(current_volume)
crash_sound.set_volume(current_volume)
coin_sound.set_volume(current_volume)
fire_sound.set_volume(current_volume)

lanes = [100, 300, 500, 700, 900]
ENEMY_SPEED = 8
INITIAL_SCROLL_SPEED = 5
INITIAL_CAR_SPEED = 7

class Weather:
    def __init__(self):
        self.current = "clear"  # default
        self.timer = 0
    
    def change_weather(self):
        weathers = ["clear", "rainy", "hot", "cold", "snowfall"]
        self.current = random.choice(weathers)
        self.timer = 600
    
    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.change_weather()
            
def draw_rain(screen):
    for _ in range(50):
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        pygame.draw.line(screen, (0, 0, 255), (x, y), (x, y+5), 1)


def draw_snow(screen):
    for _ in range(30):
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)


def draw_fog(screen):
    fog = pygame.Surface(screen.get_size())
    fog.fill((200, 200, 200))
    fog.set_alpha(100)
    screen.blit(fog, (0, 0))


def draw_heat(screen):
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((255, 200, 100))
    overlay.set_alpha(60)
    screen.blit(overlay, (0, 0))



def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, hover_color if x < mouse[0] < x+w and y < mouse[1] < y+h else color, (x, y, w, h))
    label = button_font.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return x < mouse[0] < x+w and y < mouse[1] < y+h 

def spawn_enemy(base_speed):
    vehicle = random.choice(enemy_vehicles)
    lane = random.choice(lanes)
    return {"image": vehicle, "x": lane, "y": -vehicle.get_height(), "speed": base_speed}

def game_intro():
    while True:
        screen.blit(opening_bg, (0, 0))
        title = game_over_font.render("MULTI-VEHICLE CAR GAME", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 350))
        instr_rect = pygame.Rect(WIDTH//2 + 100 , HEIGHT//2 - 100, 400, 70)
        draw_button("INSTRUCTIONS", *instr_rect, GRAY, (150, 150, 150))
        
        play_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 180, 200, 70)
        exit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 300, 200, 70)
        draw_button("PLAY", *play_rect, GREEN, (0,255,0))
        draw_button("EXIT", *exit_rect, RED, (255, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if instr_rect.collidepoint(mouse):
                    show_instructions()
                if play_rect.collidepoint(mouse):
                    return 'play'
                if exit_rect.collidepoint(mouse):
                    quit_game()
                    
def show_instructions():
    back_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 60)
    instructions = [
        "HOW TO PLAY:",
        "- Avoid enemy vehicles.",
        "- Use +/- to change volume.",
        "- Avoid fire to deduce score.",
        "- Use arrow keys to move the car.",
        "- Press SPACE to jump over obstacles.", 
        "- If fuel reaches zero, the game is over.",
        "- Reach higher levels by scoring points.",
        "- Also can use WASD keys to move the car.",
        "- Collect hearts and coins for bonus score.",
        "- Press M or Left SHIFT or Right SHIFT to mute.",
        "- Press Main ENTER or Keypad ENTER or P to pause.",
        "- The game over, when you crash into an enemy vehicle.",
        "- Fuel decreases over time; collect fuel cans to refill."
        "",
        
        "Good luck and drive safe!"
    ]

    while True:
        screen.blit(instructions_bg, (0, 0))  
        title = game_over_font.render("INSTRUCTIONS", True, RED)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # Draw instruction lines
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i * 40))

        draw_button("BACK", *back_button_rect, RED, (255, 0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse):
                    return  # Exit instruction screen
                                


def car_and_road_selection():
    global selected_car_index, selected_road_index
    cooldown_time = 200
    last_button_time = pygame.time.get_ticks()
    running = True
    result = None

    def change_car(direction):
        global selected_car_index
        selected_car_index = (selected_car_index + direction) % len(car_images)

    def change_road(direction):
        global selected_road_index
        selected_road_index = (selected_road_index + direction) % len(road_images)

    def play_and_exit():
        nonlocal running, result
        running = False
        result = 'play'

    def back_and_exit():
        nonlocal running, result
        running = False
        result = 'back'

    while running:
        screen.blit(change_bg, (0, 0))
        title = game_over_font.render("SELECT VEHICLE AND ROAD", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        car_label = font.render("Select Your Car", True, BLACK)
        screen.blit(car_label, (WIDTH // 2 - car_label.get_width() // 2, 135))
        for i, img in enumerate(car_images):
            border_color = GREEN if i == selected_car_index else BLACK
            pygame.draw.rect(screen, border_color, (WIDTH//2 - 590 + i*170, 180, 155, 220), 4)
            screen.blit(img, (WIDTH//2 - 585 + i*170, 190))
        road_label = font.render("Select Your Road", True, BLACK)
        screen.blit(road_label, (WIDTH // 2 - road_label.get_width() // 2, 520))
        screen.blit(pygame.transform.scale(road_images[selected_road_index], (300, 200)), (WIDTH//2 - 150, 565))
        current_time = pygame.time.get_ticks()
        if current_time - last_button_time > cooldown_time:
            prev_car_button_rect = pygame.Rect(WIDTH // 2 - 200, 420, 100, 50)
            next_car_button_rect = pygame.Rect(WIDTH // 2 + 100, 420, 100, 50)
            prev_road_button_rect = pygame.Rect(WIDTH // 2 - 300, 800, 250, 50)
            next_road_button_rect = pygame.Rect(WIDTH // 2 + 100, 800, 250, 50)
            draw_button("PREV", WIDTH // 2 - 200, 420, 100, 50, GREEN, (0, 255, 0))
            draw_button("NEXT", WIDTH // 2 + 100, 420, 100, 50, GREEN, (0, 255, 0))
            draw_button("PREV ROAD", WIDTH // 2 - 300, 800, 250, 50, GREEN, (0, 255, 0))
            draw_button("NEXT ROAD", WIDTH // 2 + 100, 800, 250, 50, GREEN, (0, 255, 0))
        start_button_rect = pygame.Rect(WIDTH // 2 - 220, 900, 180, 60)
        back_button_rect = pygame.Rect(WIDTH // 2 + 40, 900, 180, 60)
        draw_button("START", WIDTH // 2 - 220, 900, 180, 60, GREEN, (0, 255, 0))
        draw_button("BACK", WIDTH // 2 + 40, 900, 180, 60, RED, (255, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if prev_car_button_rect.collidepoint(mouse):
                    change_car(-1)
                if next_car_button_rect.collidepoint(mouse):
                    change_car(1)
                if prev_road_button_rect.collidepoint(mouse):
                    change_road(-1)
                if next_road_button_rect.collidepoint(mouse):
                    change_road(1)
                if start_button_rect.collidepoint(mouse):
                    play_and_exit()
                if back_button_rect.collidepoint(mouse):
                    back_and_exit()
    return result


def change_car(direction):
    global selected_car_index
    selected_car_index = (selected_car_index + direction) % len(car_images)

def pause_screen():
    resume_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 70)
    while True:
        screen.blit(gameresume_bg, (0, 0))
        paused_text = game_over_font.render("PAUSED", True, BLACK)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - 100))
        draw_button("RESUME", *resume_rect, GREEN, (0, 255, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if resume_rect.collidepoint(mouse):
                    return

def game_over_screen(score):
    name = get_player_name()
    submit_score(name, score)
    save_score_to_csv(name, score)
    leaderboard = fetch_leaderboard()

    while True:
        screen.blit(gameover_bg, (0, 0))
        over_text = game_over_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 250))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 150))

        y = HEIGHT // 2 - 20
        screen.blit(font.render("Leaderboard:", True, BLACK), (WIDTH // 2 - 80, y - 15))
        for i, entry in enumerate(leaderboard[:10]):
            y += 30
            entry_text = f"{i+1}. {entry['name']} - {entry['score']}"
            screen.blit(font.render(entry_text, True, GREEN), (WIDTH // 2 - 80, y))

        replay_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 200, 140, 60)
        exit_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 200, 140, 60)
        draw_button("REPLAY", *replay_rect, GREEN, (0,255,0))
        draw_button("EXIT", *exit_rect, RED, (255, 0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if replay_rect.collidepoint(mouse):
                    return
                if exit_rect.collidepoint(mouse):
                    quit_game()
def get_player_name():
    input_active = True
    name = ""
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    color = GRAY
    while input_active:
        screen.blit(name_input_bg, (0, 0))
        prompt = game_over_font.render("Enter Your Name", True, GREEN)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(name, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()
        clock.tick(30)
    return name.strip()

def quit_game():
    pygame.quit()
    sys.exit()

def game_loop():
    global current_volume, fuel, fuel_x, fuel_y
    car_x = WIDTH // 2 - car_images[selected_car_index].get_width() // 2
    car_y = HEIGHT - car_images[selected_car_index].get_height() - 20
    road_y = 0
    score = 0
    enemies = []
    spawn_delay = 0
    level = 1
    level_threshold = 10
    base_enemy_speed = ENEMY_SPEED
    scroll_speed = INITIAL_SCROLL_SPEED
    car_speed = INITIAL_CAR_SPEED
    game_over = False
    hearts = []
    heart_spawn_delay = 300
    coins = []
    coin_spawn_delay = 150 
    fires = []
    fire_spawn_delay = 250
    is_jumping = False
    jump_velocity = -20
    gravity = 1
    vertical_velocity = 0
    ground_y = car_y

    # --- Fuel variables ---
    fuel = 100
    fuel_decrease_rate = 0.05
    fuel_can_img = pygame.transform.scale(pygame.image.load(r".\Car_fun\game_frontend\file\oth\fuel.png"), (80, 80))
    fuel_x, fuel_y = random.randint(50, WIDTH - 50), -100
    fuel_speed = 5

    play_next_music()
    weather = Weather()

    while True:
        screen.fill(WHITE)
        road_y += scroll_speed
        if road_y >= HEIGHT:
            road_y = 0
        road_img = road_images[selected_road_index]
        screen.blit(road_img, (0, road_y - HEIGHT))
        screen.blit(road_img, (0, road_y))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_screen()

                # Volume control
                elif event.key in (pygame.K_m, pygame.K_LSHIFT, pygame.K_RSHIFT):  
                    if current_volume > 0:
                        current_volume = 0
                    else:
                        current_volume = 1.0
                    pygame.mixer.music.set_volume(current_volume)
                    jump_sound.set_volume(current_volume)
                    collect_sound.set_volume(current_volume)
                    crash_sound.set_volume(current_volume)
                    coin_sound.set_volume(current_volume)
                    fire_sound.set_volume(current_volume)
                    fuel_sound.set_volume(current_volume)

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):  # Volume down
                    current_volume = max(0, current_volume - 0.1)
                    pygame.mixer.music.set_volume(current_volume)
                    jump_sound.set_volume(current_volume)
                    collect_sound.set_volume(current_volume)
                    crash_sound.set_volume(current_volume)
                    coin_sound.set_volume(current_volume)
                    fire_sound.set_volume(current_volume)
                    fuel_sound.set_volume(current_volume)

                elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):  # Volume up
                    current_volume = min(1.0, current_volume + 0.1)
                    pygame.mixer.music.set_volume(current_volume)
                    jump_sound.set_volume(current_volume)
                    collect_sound.set_volume(current_volume)
                    crash_sound.set_volume(current_volume)
                    coin_sound.set_volume(current_volume)
                    fire_sound.set_volume(current_volume)
                    fuel_sound.set_volume(current_volume)
                    
            elif event.type == pygame.USEREVENT + 1:
                if not game_over:
                    play_next_music()
            
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_RETURN, pygame.K_KP_ENTER):
                pause_screen()

        if not game_over:
            keys = pygame.key.get_pressed()
            if not is_jumping and keys[pygame.K_SPACE]:
                is_jumping = True
                vertical_velocity = jump_velocity
                jump_sound.play()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and car_x > 0:
                car_x -= car_speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and car_x < WIDTH - car_images[selected_car_index].get_width():
                car_x += car_speed
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and car_y > 0:
                car_y -= car_speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and car_y < HEIGHT - car_images[selected_car_index].get_height():
                car_y += car_speed

            if is_jumping:
                car_y += vertical_velocity
                vertical_velocity += gravity
                if car_y >= ground_y:
                    car_y = ground_y
                    is_jumping = False

            if is_jumping:
                scale_factor = 0.85 if vertical_velocity < 0 else 0.9
                angle = -10 if vertical_velocity < 0 else 10
            else:
                scale_factor = 1.0
                angle = 0
                
            weather.update()
            
            jump_width = int(car_images[selected_car_index].get_width() * scale_factor)
            jump_height = int(car_images[selected_car_index].get_height() * scale_factor)
            scaled_car = pygame.transform.scale(car_images[selected_car_index], (jump_width, jump_height))
            rotated_car = pygame.transform.rotate(scaled_car, angle)
            car_draw_x = car_x + (car_images[selected_car_index].get_width() - jump_width) // 2
            car_draw_y = car_y + (car_images[selected_car_index].get_height() - jump_height) // 2
            screen.blit(rotated_car, (car_draw_x, car_draw_y))

            car_rect = pygame.Rect(car_x, car_y, car_images[selected_car_index].get_width(), car_images[selected_car_index].get_height())

            fuel -= fuel_decrease_rate
            if fuel <= 0:
                pygame.mixer.music.stop()
                print("Game Over - Out of Fuel!")
                game_over = True

            fuel_y += fuel_speed
            if fuel_y > HEIGHT:
                fuel_x, fuel_y = random.randint(50, WIDTH - 50), -100

            if car_rect.colliderect(pygame.Rect(fuel_x, fuel_y, 40, 40)):
                fuel = min(100, fuel + 30)
                fuel_sound.play() 
                fuel_x, fuel_y = random.randint(50, WIDTH - 50), -100

            heart_rects = [pygame.Rect(h["x"], h["y"], 50, 50) for h in hearts]
            for i, rect in enumerate(heart_rects):
                if car_rect.colliderect(rect):
                    score += 5
                    collect_sound.play()
                    del hearts[i]
                    break
            hearts = [h for h in hearts if h["y"] < HEIGHT]
            
            fire_rects = [pygame.Rect(h["x"], h["y"], 45, 45) for h in fires]
            for i, rect in enumerate(fire_rects):
                if car_rect.colliderect(rect):
                    score -= 3
                    fire_sound.play()
                    del fires[i]
                    break
            fires = [h for h in fires if h["y"] < HEIGHT]
            
            coin_rects = [pygame.Rect(c["x"], c["y"], 40, 40) for c in coins]
            for i, rect in enumerate(coin_rects):
                if car_rect.colliderect(rect):
                    score += 2
                    coin_sound.play()
                    del coins[i]
                    break
            coins = [c for c in coins if c["y"] < HEIGHT]

            # Spawn enemies
            if spawn_delay <= 0:
                occupied_lanes = [enemy["x"] for enemy in enemies if enemy["y"] < 250]
                available_lanes = [lane for lane in lanes if lane not in occupied_lanes]
                if available_lanes:
                    new_enemy = spawn_enemy(base_enemy_speed)
                    new_enemy["x"] = random.choice(available_lanes)
                    enemies.append(new_enemy)
                    score += 1
                    spawn_delay = random.randint(30, 60)
            else:
                spawn_delay -= 1

            # Spawn hearts
            if heart_spawn_delay <= 0:
                lane = random.choice(lanes)
                hearts.append({"x": lane + 50, "y": -50})
                heart_spawn_delay = random.randint(600, 1000)
            else:
                heart_spawn_delay -= 1
                
            # Spawn fires
            if fire_spawn_delay <= 0:
                lane = random.choice(lanes)
                fires.append({"x": lane + 50, "y": -50})
                fire_spawn_delay = random.randint(600, 1000)
            else:
                fire_spawn_delay -= 1
                
            # Spawn coins
            if coin_spawn_delay <= 0:
                lane = random.choice(lanes)
                coins.append({"x": lane + 60, "y": -50})
                coin_spawn_delay = random.randint(200, 400)
            else:
                coin_spawn_delay -= 1

            for enemy in enemies:
                enemy["y"] += enemy["speed"]
                screen.blit(enemy["image"], (enemy["x"], enemy["y"]))
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 150, 200)
                if not is_jumping and car_rect.colliderect(enemy_rect):
                    pygame.mixer.music.stop()
                    crash_sound.play()
                    game_over = True

            enemies = [e for e in enemies if e["y"] < HEIGHT]

            for heart in hearts:
                heart["y"] += scroll_speed
                screen.blit(heart_image, (heart["x"], heart["y"]))
                
            for fire in fires:
                fire["y"] += scroll_speed
                screen.blit(fire_image, (fire["x"], fire["y"]))
                
            for coin in coins:
                coin["y"] += scroll_speed
                screen.blit(coin_image, (coin["x"], coin["y"]))

            # Draw fuel collectible
            screen.blit(fuel_can_img, (fuel_x, fuel_y))

            # Draw fuel bar
            pygame.draw.rect(screen, (0, 0, 0), (10, 80, 200, 20))  
            pygame.draw.rect(screen, (255, 255, 0), (10, 80, int(fuel * 2), 20))

            # Level up
            while score >= level_threshold:
                level += 1
                base_enemy_speed += 1
                scroll_speed += 1
                car_speed += 0.5
                level_threshold += 20

            score_text = font.render(f"Score: {score}", True, BLACK)
            level_text = font.render(f"Level: {level}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
        else:
            game_over_screen(score)
            return

        if weather.current == "rainy":
            draw_rain(screen)
        elif weather.current == "snowfall":
            draw_snow(screen)
        elif weather.current == "cold":
            draw_fog(screen)
        elif weather.current == "hot":
            draw_heat(screen)

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        intro_result = game_intro()
        if intro_result == 'play':
            while True:
                selection_result = car_and_road_selection()
                if selection_result == 'play':
                    game_loop()
                    break
                elif selection_result == 'back':
                    break

if __name__ == "__main__":
    main()