import pygame
import random
import time
import sys
import os
from sci_dama import SciDamaGame

# --- High Score Utilities ---
def get_high_score(difficulty):
    filename = f"highscore_{difficulty.lower()}.txt"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return int(f.read())
        except:
            return 0
    else:
        return 0

def save_high_score(difficulty, score):
    filename = f"highscore_{difficulty.lower()}.txt"
    try:
        with open(filename, "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

pygame.mixer.pre_init(44100, -16, 2, 512)  # Optional: better sound quality settings
pygame.mixer.init()

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Rush & Sci-Dama")

try:
    pygame.mixer.music.load("little town - orchestral.ogg")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print("Could not load music file:", e)

try:
    menu_background = pygame.image.load("select_menu_background.jpg")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
except:
    menu_background = None

try:
    select_menu_background = pygame.image.load("select_menu_background.jpg")
    select_menu_background = pygame.transform.scale(select_menu_background, (WIDTH, HEIGHT))
except:
    select_menu_background = None

try:
    settings_menu_background = pygame.image.load("settings.png")
    settings_menu_background = pygame.transform.scale(settings_menu_background, (WIDTH, HEIGHT))
except:
    settings_menu_background = None

try:
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = None

try:
    correct_sound = pygame.mixer.Sound("correct.wav")
    correct_sound.set_volume(0.7)  # Adjust as needed
except pygame.error as e:
    print("Could not load correct sound:", e)
    correct_sound = None    

try:
    wrong_sound = pygame.mixer.Sound("wrong.mp3")
    wrong_sound.set_volume(0.7)  # Adjust as needed
except pygame.error as e:
    print("Could not load correct sound:", e)
    wrong_sound = None 

FONT = pygame.font.SysFont("Arial", 36)
SMALL_FONT = pygame.font.SysFont("Arial", 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
MENU_COLOR = (100, 100, 200)

# Default timer value (can be changed in settings)
selected_timer = 10

class Button:
    def __init__(self, x, y, w, h, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        txt = FONT.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def generate_question(level):
    if level == 1:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-'])
    elif level == 2:
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*'])
    else:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        op = random.choice(['+', '-', '*', '/'])
        if op == '/':
            a = a * b  # Ensure integer division

    if op == '+':
        answer = a + b
    elif op == '-':
        answer = a - b
    elif op == '*':
        answer = a * b
    elif op == '/':
        answer = a // b

    question = f"{a} {op} {b} = ?"
    return question, answer

def main_menu():
    menu = True
    clock = pygame.time.Clock()

    math_button = Button(WIDTH//2 - 100, 220, 200, 50, "Math Rush", BLACK)
    sci_button = Button(WIDTH//2 - 100, 280, 200, 50, "Sci-Dama", BLUE)
    settings_button = Button(WIDTH//2 - 100, 340, 200, 50, "Settings", GREEN)
    quit_button = Button(WIDTH//2 - 100, 400, 200, 50, "Quit", RED)

    while menu:
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill((100, 100, 200))

        title = FONT.render("MAIN MENU", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        math_button.draw(screen)
        sci_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if math_button.is_clicked(pos):
                    difficulty_select_menu()
                elif sci_button.is_clicked(pos):
                    game = SciDamaGame(screen, WIDTH, HEIGHT)
                    game.run()
                elif settings_button.is_clicked(pos):
                    settings_menu()
                elif quit_button.is_clicked(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

def difficulty_select_menu():
    menu = True
    clock = pygame.time.Clock()

    normal_button = Button(WIDTH//2 - 100, 220, 200, 50, "Easy", GREEN)
    medium_button = Button(WIDTH//2 - 100, 300, 200, 50, "Medium", BLUE)
    hard_button = Button(WIDTH//2 - 100, 380, 200, 50, "Hard", RED)
    back_button = Button(20, 20, 100, 40, "Back", BLUE)

    while menu:
        if select_menu_background:
            screen.blit(select_menu_background, (0, 0))
        else:
            screen.fill((100, 100, 200))

        title = FONT.render("Select Difficulty", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        normal_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if normal_button.is_clicked(pos):
                    math_rush_game("Easy", selected_timer)
                elif medium_button.is_clicked(pos):
                    math_rush_game("Medium", selected_timer)
                elif hard_button.is_clicked(pos):
                    math_rush_game("Hard", selected_timer)
                elif back_button.is_clicked(pos):
                    menu = False

        pygame.display.flip()
        clock.tick(60)

def settings_menu():
    global selected_timer
    menu = True
    clock = pygame.time.Clock()

    timer_buttons = [
        Button(WIDTH//2 - 220, 220, 120, 60, "5 Sec", BLUE),
        Button(WIDTH//2 - 80, 220, 120, 60, "10 Sec", BLUE),
        Button(WIDTH//2 + 60, 220, 120, 60, "15 Sec", BLUE),
        Button(WIDTH//2 - 220, 320, 120, 60, "20 Sec", BLUE),
        Button(WIDTH//2 - 80, 320, 120, 60, "25 Sec", BLUE),
        Button(WIDTH//2 + 60, 320, 120, 60, "30 Sec", BLUE),
    ]
    back_button = Button(20, 20, 100, 40, "Back", BLUE)

    while menu:
        if settings_menu_background:
            screen.blit(settings_menu_background, (0, 0))
        else:
            screen.fill((100, 100, 200))

        for btn in timer_buttons:
            btn.draw(screen)

        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, btn in enumerate(timer_buttons):
                    if btn.is_clicked(pos):
                        selected_timer = 5 + idx * 5
                        menu = False
                        return  # Go back to main menu immediately
                if back_button.is_clicked(pos):
                    menu = False

        pygame.display.flip()
        clock.tick(60)

def math_rush_game(difficulty_level, question_timeout):
    high_score = get_high_score(difficulty_level)
    clock = pygame.time.Clock()
    input_text = ''
    score = 0
    streak = 0
    round_num = 1
    max_rounds = 10
    feedback = ''
    feedback_color = GREEN

    level_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    level = level_map.get(difficulty_level, 1)

    question, answer = generate_question(level)
    question_start_time = time.time()

    submit_button = Button(WIDTH//2 - 60, HEIGHT - 100, 120, 50, "Submit", BLUE)
    back_button = Button(WIDTH - 120, HEIGHT - 60, 100, 40, "Back", RED)

    running = True
    while running:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((255, 255, 255))

        # Display high score at top left
        high_score_text = SMALL_FONT.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(high_score_text, (20, 10))

        # Draw back button
        back_button.draw(screen)

        current_time = time.time()
        elapsed_time = current_time - question_start_time
        remaining_time = max(0, question_timeout - elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return  # Go back to difficulty menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text.strip() != '':
                        try:
                            user_answer = int(input_text)
                        except ValueError:
                            feedback = "Please enter a valid number!"
                            feedback_color = RED
                            input_text = ''
                            continue

                        if user_answer == answer and elapsed_time <= question_timeout:
                            if correct_sound:
                                correct_sound.play()
                            feedback = "Correct!"
                            feedback_color = GREEN
                            score += 1
                            streak += 1
                            if streak >= 3 and level < 3:
                                level += 1
                                feedback += " Level up!"
                                streak = 0
                        else:
                            if wrong_sound:
                                wrong_sound.play()
                            feedback = f"Wrong or too slow! Answer was {answer}."
                            feedback_color = RED
                            streak = 0
                            if level > 1:
                                level -= 1
                                feedback += " Level down!"

                        round_num += 1
                        if round_num > max_rounds:
                            running = False
                        else:
                            question, answer = generate_question(level)
                            question_start_time = time.time()
                            input_text = ''
                            remaining_time = question_timeout

                else:
                    if event.unicode.isdigit() or (event.unicode == '-' and len(input_text) == 0):
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.is_clicked(event.pos):
                    if input_text.strip() != '':
                        try:
                            user_answer = int(input_text)
                        except ValueError:
                            feedback = "Please enter a valid number!"
                            feedback_color = RED
                            input_text = ''
                            continue

                        if user_answer == answer and elapsed_time <= question_timeout:
                            feedback = "Correct!"
                            feedback_color = GREEN
                            score += 1
                            streak += 1
                            if streak >= 3 and level < 3:
                                level += 1
                                feedback += " Level up!"
                                streak = 0
                        else:
                            feedback = f"Wrong or too slow! Answer was {answer}."
                            feedback_color = RED
                            streak = 0
                            if level > 1:
                                level -= 1
                                feedback += " Level down!"

                        round_num += 1
                        if round_num > max_rounds:
                            running = False
                        else:
                            question, answer = generate_question(level)
                            question_start_time = time.time()
                            input_text = ''
                            remaining_time = question_timeout

        if remaining_time <= 0:
            feedback = f"Time's up! The correct answer was {answer}."
            feedback_color = RED
            streak = 0

            round_num += 1
            if round_num > max_rounds:
                running = False
            else:
                question, answer = generate_question(level)
                question_start_time = time.time()
                input_text = ''
                remaining_time = question_timeout

        # --- Centered Drawing ---

        # Round info centered at top (below high score)
        round_text = FONT.render(f"Round {round_num} of {max_rounds}", True, BLACK)
        round_rect = round_text.get_rect(center=(WIDTH // 2, 65))
        screen.blit(round_text, round_rect)

        # Question centered horizontally
        question_text = FONT.render(question, True, BLACK)
        question_rect = question_text.get_rect(center=(WIDTH // 2, 158))
        screen.blit(question_text, question_rect)

        # Input box centered horizontally
        input_box_width, input_box_height = 300, 60
        input_box_x = (WIDTH - input_box_width) // 2
        input_box_y = 180
        input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(screen, GRAY, input_box, border_radius=8)

        # User input text inside input box with padding
        input_surface = FONT.render(input_text, True, BLACK)
        input_text_x = input_box.x + 15
        input_text_y = input_box.y + (input_box.height - input_surface.get_height()) // 2
        screen.blit(input_surface, (input_text_x, input_text_y))

        # Feedback message below input box
        feedback_surface = SMALL_FONT.render(feedback, True, feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(WIDTH // 2, input_box_y + input_box_height + 217))
        screen.blit(feedback_surface, feedback_rect)

        # Score and difficulty info top-right
        score_surface = SMALL_FONT.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (WIDTH - 150, 20))

        level_surface = SMALL_FONT.render(f"Difficulty: {difficulty_level}", True, BLACK)
        screen.blit(level_surface, (WIDTH - 200, 60))

        # Timer bottom-left
        timer_text = FONT.render(f"Time: {int(remaining_time)}", True, BLACK)
        screen.blit(timer_text, (20, HEIGHT - 50))

        # Submit button centered horizontally near bottom
        submit_button.rect.centerx = WIDTH // 2
        submit_button.rect.y = HEIGHT - 100
        submit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    # After game ends, save new high score if beaten
    if score > high_score:
        save_high_score(difficulty_level, score)

    # Game over screen
    screen.fill(WHITE)
    if background:
        screen.blit(background, (0, 0))

    game_over_text = FONT.render("Game Over!", True, BLACK)
    score_text = FONT.render(f"Your Score: {score} / {max_rounds}", True, BLACK)
    high_score_text = FONT.render(f"High Score: {max(score, high_score)}", True, GREEN if score > high_score else BLACK)

    if score >= 8:
        message = "Excellent work! You're a math star!"
    elif score >= 5:
        message = "Good job! Keep practicing!"
    else:
        message = "Don't give up! Try again to improve!"

    message_text = SMALL_FONT.render(message, True, BLACK)

    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//10))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//7 + 35))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//6 + 60))
    screen.blit(message_text, (WIDTH//2 - message_text.get_width()//2, HEIGHT//2 + 145))

    pygame.display.flip()
    pygame.time.wait(5000)
    difficulty_select_menu()

if __name__ == "__main__":
    main_menu()
