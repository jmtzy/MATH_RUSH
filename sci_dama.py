import pygame
import sys
import random
import time

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()


# Load menu background once for use in menus
try:
    menu_background = pygame.image.load("bg.png")
    menu_background = pygame.transform.scale(menu_background, (800, 600))  # Or use your WIDTH, HEIGHT if defined
except:
    menu_background = None

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

try:
    move_sound = pygame.mixer.Sound("move.mp3")
    move_sound.set_volume(0.7)  # Adjust as needed
except pygame.error as e:
    print("Could not load correct sound:", e)
    move_sound = None

class SciDamaGame:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.INFO_WIDTH = 200
        self.BOARD_WIDTH = self.WIDTH - self.INFO_WIDTH
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = min(self.BOARD_WIDTH, self.HEIGHT) // self.COLS
        self.PIECE_RADIUS = self.SQUARE_SIZE // 2 - 10
        self.correct_sound = pygame.mixer.Sound("correct.wav")
        self.correct_sound.set_volume(0.7)  # Adjust as needed
        self.wrong_sound = pygame.mixer.Sound("wrong.mp3")
        self.wrong_sound.set_volume(0.7)
        self.move_sound = pygame.mixer.Sound("move.mp3")  # Use your sound file name
        self.move_sound.set_volume(0.5)  # Adjust volume as needed



        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BOARD_WHITE = (230, 230, 230)
        self.BOARD_BLACK = (70, 70, 70)
        self.RED = (200, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.GOLD = (255, 215, 0)

        # Fonts
        self.FONT = pygame.font.SysFont("Arial", 32)
        self.SMALL_FONT = pygame.font.SysFont("Arial", 20)
        self.PIECE_FONT = pygame.font.SysFont("Arial", 20, bold=True)
        self.KING_FONT = pygame.font.SysFont("Arial", 18, bold=True)

        # Game state
        self.difficulty = "Easy"
        self.question_timer = 15
        self.operation = '+'
        self.board, self.numbers, self.kings = self.create_board()
        self.selected = None
        self.valid_moves = []
        self.player_color = 2  # Always Blue at bottom
        self.ai_color = 1      # Always Red at top
        self.turn = self.player_color
        self.red_pieces = 12
        self.blue_pieces = 12
        self.player_score = 0
        self.ai_score = 0

    def create_board(self):
        board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        numbers = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        kings = [[False for _ in range(self.COLS)] for _ in range(self.ROWS)]
        if self.difficulty == "Easy":
            num_min, num_max = 1, 6
        elif self.difficulty == "Medium":
            num_min, num_max = 4, 12
        else:
            num_min, num_max = 8, 20
        for row in range(3):
            for col in range(self.COLS):
                if (row + col) % 2 == 1:
                    board[row][col] = 1
                    numbers[row][col] = random.randint(num_min, num_max)
        for row in range(5, 8):
            for col in range(self.COLS):
                if (row + col) % 2 == 1:
                    board[row][col] = 2
                    numbers[row][col] = random.randint(num_min, num_max)
        return board, numbers, kings

    def draw_board(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = self.BOARD_WHITE if (row + col) % 2 == 1 else self.BOARD_BLACK
                pygame.draw.rect(self.screen, color,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                  self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece_color = self.RED if piece == 1 else self.BLUE
                    center = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                              row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                    pygame.draw.circle(self.screen, piece_color, center, self.PIECE_RADIUS)
                    # Draw piece number
                    num = self.numbers[row][col]
                    num_surf = self.PIECE_FONT.render(str(num), True, self.WHITE)
                    num_rect = num_surf.get_rect(center=center)
                    self.screen.blit(num_surf, num_rect)
                    # Draw king marker
                    if self.kings[row][col]:
                        pygame.draw.circle(self.screen, self.GOLD, center, self.PIECE_RADIUS // 2, 3)
                        king_surf = self.KING_FONT.render("K", True, self.GOLD)
                        king_rect = king_surf.get_rect(center=(center[0], center[1]+16))
                        self.screen.blit(king_surf, king_rect)
        # Highlight selected piece
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, self.GREEN,
                             (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                              self.SQUARE_SIZE, self.SQUARE_SIZE), 4)
        # Highlight valid moves
        if self.selected:
            for move in self.valid_moves:
                if isinstance(move, tuple) and isinstance(move[0], tuple):
                    dest_row, dest_col = move[0]
                else:
                    dest_row, dest_col = move
                center = (dest_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                          dest_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, self.GREEN, center, self.PIECE_RADIUS // 2, 3)

    def draw_scores(self):
        pygame.draw.rect(self.screen, self.GRAY, 
                         (self.BOARD_WIDTH, 0, self.INFO_WIDTH, self.HEIGHT), border_radius=16)

        y = 30
        self.screen.blit(self.SMALL_FONT.render("🟦 PLAYER", True, self.BLUE), (self.BOARD_WIDTH + 10, y))
        y += 22
        self.screen.blit(self.SMALL_FONT.render(f"Score: {self.player_score}", True, self.BLUE), (self.BOARD_WIDTH + 10, y))
        y += 24
        self.screen.blit(self.SMALL_FONT.render("🟥 AI", True, self.RED), (self.BOARD_WIDTH + 10, y))
        y += 22
        self.screen.blit(self.SMALL_FONT.render(f"Score: {self.ai_score}", True, self.RED), (self.BOARD_WIDTH + 10, y))
        y += 24
        self.screen.blit(self.SMALL_FONT.render(f"Operation: {self.operation}", True, self.BLACK), (self.BOARD_WIDTH + 10, y))
        y += 24
        self.screen.blit(self.SMALL_FONT.render(f"Turn: {'Player' if self.turn == self.player_color else 'AI'}", True, self.BLACK), (self.BOARD_WIDTH + 10, y))
        y += 24
        self.screen.blit(self.SMALL_FONT.render(f"Difficulty: {self.difficulty}", True, self.BLACK), (self.BOARD_WIDTH + 10, y))

    def select_difficulty_menu(self):
        clock = pygame.time.Clock()
        easy_btn = Button((self.WIDTH // 2) - 210, self.HEIGHT // 2, 120, 50, "Easy", self.GREEN)
        medium_btn = Button((self.WIDTH // 2) - 70, self.HEIGHT // 2, 120, 50, "Medium", self.BLUE)
        hard_btn = Button((self.WIDTH // 2) + 70, self.HEIGHT // 2, 120, 50, "Hard", self.RED)
        selecting = True
        while selecting:
            clock.tick(60)
            if menu_background:
                self.screen.blit(menu_background, (0, 0))
            else:
                self.screen.fill(self.GRAY)

            title = self.FONT.render("Select Difficulty", True, self.BLACK)
            self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 15)))
            easy_btn.draw(self.screen)
            medium_btn.draw(self.screen)
            hard_btn.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if easy_btn.is_clicked(pos):
                        self.difficulty = "Easy"
                        self.question_timer = 15
                        selecting = False
                    elif medium_btn.is_clicked(pos):
                        self.difficulty = "Medium"
                        self.question_timer = 12
                        selecting = False
                    elif hard_btn.is_clicked(pos):
                        self.difficulty = "Hard"
                        self.question_timer = 10
                        selecting = False
            pygame.display.flip()

    def select_operation_menu(self):
        clock = pygame.time.Clock()
        add_btn = Button((self.WIDTH // 2) - 210, self.HEIGHT // 2, 100, 50, "Add", self.GREEN)
        sub_btn = Button((self.WIDTH // 2) - 70, self.HEIGHT // 2, 100, 50, "Subtract", self.BLUE)
        mul_btn = Button((self.WIDTH // 2) + 70, self.HEIGHT // 2, 100, 50, "Multiply", self.RED)
        div_btn = Button((self.WIDTH // 2) + 210, self.HEIGHT // 2, 100, 50, "Divide", self.GRAY)
        back_button = Button((self.WIDTH // 2) - 60, self.HEIGHT // 2 + 80, 120, 40, "Back", self.BLACK)
        selecting = True
        while selecting:
            clock.tick(60)
            if menu_background:
                self.screen.blit(menu_background, (0, 0))
            else:
                self.screen.fill(self.GRAY)
            
            title = self.FONT.render("Choose Arithmetic Operation", True, self.BLACK)
            self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 15)))
            add_btn.draw(self.screen)
            sub_btn.draw(self.screen)
            mul_btn.draw(self.screen)
            div_btn.draw(self.screen)
            back_button.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if add_btn.is_clicked(pos):
                        self.operation = '+'
                        selecting = False
                    elif sub_btn.is_clicked(pos):
                        self.operation = '-'
                        selecting = False
                    elif mul_btn.is_clicked(pos):
                        self.operation = '*'
                        selecting = False
                    elif div_btn.is_clicked(pos):
                        self.operation = '/'
                        selecting = False
                    elif back_button.is_clicked(pos):
                        self.select_difficulty_menu()
            pygame.display.flip()

    def get_valid_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        is_king = self.kings[row][col]
        if piece == 0:
            return moves
        directions = []
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            direction = 1 if piece == 1 else -1
            directions = [(direction, -1), (direction, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if is_king:
                # King can move/capture any distance
                while 0 <= r < self.ROWS and 0 <= c < self.COLS:
                    if self.board[r][c] == 0:
                        moves.append((r, c))
                    elif self.board[r][c] != piece:
                        jump_r, jump_c = r + dr, c + dc
                        while 0 <= jump_r < self.ROWS and 0 <= jump_c < self.COLS and self.board[jump_r][jump_c] == 0:
                            moves.append(((jump_r, jump_c), (r, c)))
                            jump_r += dr
                            jump_c += dc
                        break
                    else:
                        break
                    r += dr
                    c += dc
            else:
                if 0 <= r < self.ROWS and 0 <= c < self.COLS:
                    if self.board[r][c] == 0:
                        moves.append((r, c))
                    elif self.board[r][c] != piece:
                        jump_r = r + dr
                        jump_c = c + dc
                        if 0 <= jump_r < self.ROWS and 0 <= jump_c < self.COLS:
                            if self.board[jump_r][jump_c] == 0:
                                moves.append(((jump_r, jump_c), (r, c)))
        return moves

    def ask_math_question(self, num1, num2):
        if self.operation == '+':
            question = f"{num1} + {num2} = ?"
            answer = num1 + num2
        elif self.operation == '-':
            question = f"{num1} - {num2} = ?"
            answer = num1 - num2
        elif self.operation == '*':
            question = f"{num1} * {num2} = ?"
            answer = num1 * num2
        elif self.operation == '/':
            if num2 == 0:
                num2 = 1
            question = f"{num1} / {num2} = ?"
            answer = num1 // num2
        else:
            question = f"{num1} + {num2} = ?"
            answer = num1 + num2
        return self.popup_question(question, answer)

    def popup_question(self, question, answer):
        input_text = ''
        clock = pygame.time.Clock()
        start_time = time.time()
        while True:
            clock.tick(60)
            self.screen.fill(self.GRAY)
            qsurf = self.FONT.render(question, True, self.BLACK)
            self.screen.blit(qsurf, qsurf.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3)))
            insurf = self.FONT.render(input_text, True, self.BLACK)
            self.screen.blit(insurf, insurf.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)))
            remaining = max(0, int(self.question_timer - (time.time() - start_time)))
            timer_surf = self.SMALL_FONT.render(f"Time left: {remaining}", True, self.RED if remaining <= 3 else self.BLACK)
            self.screen.blit(timer_surf, timer_surf.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 40)))
            prompt = self.SMALL_FONT.render("Type answer and press Enter", True, self.BLACK)
            self.screen.blit(prompt, prompt.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 65)))
            pygame.display.flip()
            if remaining == 0:
                return False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            if int(input_text) == answer:
                                self.correct_sound.play()
                                return True
                            else:
                                self.wrong_sound.play()
                                return False
                        except:
                            input_text = ''
                    elif event.unicode.isdigit() or (event.unicode == '-' and len(input_text) == 0):
                        input_text += event.unicode

    def move_piece(self, start, end):
        self.move_sound.play()
        sr, sc = start
        if isinstance(end, tuple) and len(end) == 2 and isinstance(end[0], int):
            er, ec = end
            captured = None
        else:
            (er, ec), (cr, cc) = end
            captured = (cr, cc)
        piece = self.board[sr][sc]
        num_piece = self.numbers[sr][sc]
        is_king = self.kings[sr][sc]
        self.board[sr][sc] = 0
        self.numbers[sr][sc] = 0
        self.kings[sr][sc] = False
        self.board[er][ec] = piece
        self.numbers[er][ec] = num_piece
        self.kings[er][ec] = is_king

        # King promotion
        if not is_king:
            if piece == 2 and er == 0:
                self.kings[er][ec] = True
            elif piece == 1 and er == self.ROWS - 1:
                self.kings[er][ec] = True

        if captured:
            captured_piece = self.board[cr][cc]
            captured_num = self.numbers[cr][cc]
            if piece == self.player_color:
                correct = self.ask_math_question(num_piece, captured_num)
                if correct:
                    self.board[cr][cc] = 0
                    self.numbers[cr][cc] = 0
                    self.kings[cr][cc] = False
                    self.player_score += self.calculate_score(num_piece, captured_num)
                    if captured_piece == 1:
                        self.red_pieces -= 1
                    else:
                        self.blue_pieces -= 1
                else:
                    self.player_score -= num_piece
                    self.board[sr][sc] = piece
                    self.numbers[sr][sc] = num_piece
                    self.kings[sr][sc] = is_king
                    self.board[er][ec] = 0
                    self.numbers[er][ec] = 0
                    self.kings[er][ec] = False
            else:  # AI move: always succeeds, just add to AI score
                self.board[cr][cc] = 0
                self.numbers[cr][cc] = 0
                self.kings[cr][cc] = False
                self.ai_score += self.calculate_score(num_piece, captured_num)
                if captured_piece == 1:
                    self.red_pieces -= 1
                else:
                    self.blue_pieces -= 1

    def calculate_score(self, num1, num2):
        if self.operation == '+':
            return num1 + num2
        elif self.operation == '-':
            return num1 - num2
        elif self.operation == '*':
            return num1 * num2
        elif self.operation == '/':
            return num1 // (num2 if num2 != 0 else 1)
        else:
            return num1 + num2

    def ai_move(self):
        pieces = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.board[r][c] == self.ai_color:
                    pieces.append((r, c))
        if self.difficulty == "Easy":
            random.shuffle(pieces)
            for piece in pieces:
                moves = self.get_valid_moves(*piece)
                if moves:
                    move = random.choice(moves)
                    self.move_piece(piece, move)
                    return True
        elif self.difficulty == "Medium":
            for piece in pieces:
                moves = self.get_valid_moves(*piece)
                jumps = [m for m in moves if isinstance(m, tuple) and isinstance(m[0], tuple)]
                if jumps:
                    self.move_piece(piece, random.choice(jumps))
                    return True
            for piece in pieces:
                moves = self.get_valid_moves(*piece)
                if moves:
                    self.move_piece(piece, random.choice(moves))
                    return True
        else:  # Hard
            best_score = -float('inf')
            best_move = None
            for piece in pieces:
                moves = self.get_valid_moves(*piece)
                for m in moves:
                    if isinstance(m, tuple) and isinstance(m[0], tuple):
                        (er, ec), (cr, cc) = m
                        score = self.calculate_score(self.numbers[piece[0]][piece[1]], self.numbers[cr][cc])
                        if score > best_score:
                            best_score = score
                            best_move = (piece, m)
            if best_move:
                self.move_piece(best_move[0], best_move[1])
                return True
            for piece in pieces:
                moves = self.get_valid_moves(*piece)
                if moves:
                    self.move_piece(piece, random.choice(moves))
                    return True
        return False

    def has_any_moves(self, color):
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.board[r][c] == color and self.get_valid_moves(r, c):
                    return True
        return False

    def run(self):
        running = True
        self.select_difficulty_menu()
        self.select_operation_menu()
        self.board, self.numbers, self.kings = self.create_board()
        self.selected = None
        self.valid_moves = []
        self.red_pieces = 12
        self.blue_pieces = 12
        self.player_score = 0
        self.ai_score = 0
        self.turn = self.player_color  # Player always starts
        back_button = Button(self.BOARD_WIDTH + 40, self.HEIGHT - 60, 120, 40, "Back", self.BLACK)
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            self.screen.fill(self.BOARD_BLACK)
            self.draw_board()
            self.draw_pieces()
            self.draw_scores()
            back_button.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if back_button.is_clicked(pos):
                        running = False
                        break
                    col = pos[0] // self.SQUARE_SIZE
                    row = pos[1] // self.SQUARE_SIZE
                    if 0 <= row < self.ROWS and 0 <= col < self.COLS and self.turn == self.player_color:
                        if self.selected:
                            valid_moves = self.get_valid_moves(self.selected[0], self.selected[1])
                            valid_move_coords = [m[0] if isinstance(m, tuple) and isinstance(m[0], tuple) else m for m in valid_moves]
                            if (row, col) in valid_move_coords:
                                for m in valid_moves:
                                    if isinstance(m, tuple) and isinstance(m[0], tuple):
                                        if m[0] == (row, col):
                                            move = m
                                            break
                                    else:
                                        if m == (row, col):
                                            move = m
                                            break
                                self.move_piece(self.selected, move)
                                self.selected = None
                                self.valid_moves = []
                                self.turn = self.ai_color
                            else:
                                if self.board[row][col] == self.player_color:
                                    self.selected = (row, col)
                                    self.valid_moves = self.get_valid_moves(row, col)
                                else:
                                    self.selected = None
                                    self.valid_moves = []
                        else:
                            if self.board[row][col] == self.player_color:
                                self.selected = (row, col)
                                self.valid_moves = self.get_valid_moves(row, col)
            if self.turn == self.ai_color and running:
                pygame.time.delay(500)
                self.ai_move()
                self.selected = None
                self.valid_moves = []
                self.turn = self.player_color
            # Win condition: no pieces or no moves
            if self.red_pieces == 0 or not self.has_any_moves(self.ai_color):
                winner = "Player (Blue) Wins!" if self.player_score >= self.ai_score else "AI (Red) Wins!"
                self.show_winner(winner)
                running = False
            elif self.blue_pieces == 0 or not self.has_any_moves(self.player_color):
                winner = "AI (Red) Wins!" if self.ai_score >= self.player_score else "Player (Blue) Wins!"
                self.show_winner(winner)
                running = False
            pygame.display.flip()

    def show_winner(self, message):
        self.screen.fill(self.BLACK)
        text = self.FONT.render(message, True, self.WHITE)
        score = self.FONT.render(f"Player: {self.player_score} | AI: {self.ai_score}", True, self.WHITE)
        rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 30))
        score_rect = score.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 30))
        self.screen.blit(text, rect)
        self.screen.blit(score, score_rect)
        pygame.display.flip()
        pygame.time.wait(4000)

class Button:
    def __init__(self, x, y, w, h, text, color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.FONT = pygame.font.SysFont("Arial", 22)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        txt = self.FONT.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sci-Dama")
    game = SciDamaGame(screen, screen_width, screen_height)
    game.run()
