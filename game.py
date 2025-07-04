import pygame
import random
import time

pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SimpleTrainer")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (70, 70, 70)
LIGHT_BG = (240, 240, 240)
DARK_BG = (30, 30, 30)

best_reaction = None
best_wpm = None

def draw_text(text, x, y, color=WHITE, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect

def show_best_scores(bg_color):
    def is_dark(color):
        return sum(color) / 3 < 128
    text_color = WHITE if is_dark(bg_color) else BLACK

    padding = 10
    x = width - padding
    y = padding

    texts = []
    if best_reaction is not None:
        texts.append(f"Best Reaction: {int(best_reaction)} ms")
    else:
        texts.append("Best Reaction: N/A")

    if best_wpm is not None:
        texts.append(f"Best Typing: {int(best_wpm)} WPM")
    else:
        texts.append("Best Typing: N/A")

    for i, txt in enumerate(texts):
        surface = font.render(txt, True, text_color)
        rect = surface.get_rect(topright=(x, y + i * (surface.get_height() + 5)))
        screen.blit(surface, rect)

def menu_selection(options, title="Choose", y_start=200, bg_color=BLACK):
    while True:
        screen.fill(bg_color)
        draw_text(title, width // 2, 100, center=True, color=WHITE if sum(bg_color)/3 < 128 else BLACK)
        buttons = []
        for i, option in enumerate(options):
            color = WHITE if sum(bg_color)/3 < 128 else BLACK
            rect = draw_text(option, width // 2, y_start + i * 60, center=True, color=color)
            buttons.append((rect, option))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, value in buttons:
                    if rect.collidepoint(pos):
                        return value
        clock.tick(30)

def typing_trainer(bg_color):
    global best_wpm
    texts = [
        "still leave each other and want to be first.",
        "Typing speed is a useful skill.",
        "Practice makes perfect.",
        "Python is a great programming language."
    ]
    target = random.choice(texts)
    typed = ""
    start = None
    done = False

    while not done:
        screen.fill(bg_color)
        color_text = WHITE if sum(bg_color)/3 < 128 else BLACK
        draw_text("Typing Trainer", width // 2, 50, center=True, color=color_text)
        draw_text("Type this:", 50, 120, color=color_text)
        draw_text(target, 50, 160, color=color_text)
        draw_text("Your input:", 50, 230, color=color_text)
        draw_text(typed, 50, 270, color=color_text)

        show_best_scores(bg_color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                elif event.key == pygame.K_RETURN:
                    if typed == target:
                        done = True
                else:
                    if event.unicode.isprintable():
                        if start is None:
                            start = time.time()
                        typed += event.unicode

        clock.tick(60)

    end = time.time()
    duration = end - start if start else 0.0001
    wpm = len(target.split()) / (duration / 60)

    if (best_wpm is None) or (wpm > best_wpm):
        best_wpm = wpm

    screen.fill(bg_color)
    draw_text(f"Done! Your typing speed: {int(wpm)} WPM", width // 2, height // 2, center=True, color=color_text)
    show_best_scores(bg_color)
    pygame.display.flip()
    pygame.time.wait(3000)

def run_reaction_game(bg_color):
    global best_reaction
    difficulty = menu_selection(["Easy", "Normal", "Hard"], "Select Difficulty", bg_color=bg_color)
    radius = {"Easy": 50, "Normal": 30, "Hard": 15}[difficulty]

    mode = menu_selection(["Clicks Mode", "Time Limit Mode"], "Choose Game Mode", bg_color=bg_color)
    if mode == "Clicks Mode":
        clicks_text = menu_selection(["10", "50", "100"], "Number of targets", bg_color=bg_color)
        total_clicks = int(clicks_text)
        time_limit = None
    else:
        time_text = menu_selection(["10", "30", "60"], "Time limit in seconds", bg_color=bg_color)
        time_limit = int(time_text)
        total_clicks = None

    reaction_times = []
    score = 0
    circle_visible = False
    circle_pos = (0, 0)
    start_time = time.time()
    next_circle_time = start_time
    game_start_time = time.time()

    running = True
    while running:
        screen.fill(bg_color)
        now = time.time()

        if not circle_visible and now >= next_circle_time:
            circle_pos = (
                random.randint(radius, width - radius),
                random.randint(radius, height - radius)
            )
            circle_visible = True
            appear_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and circle_visible:
                mx, my = pygame.mouse.get_pos()
                dx = mx - circle_pos[0]
                dy = my - circle_pos[1]
                if dx ** 2 + dy ** 2 <= radius ** 2:
                    reaction_time = (now - appear_time) * 1000
                    reaction_times.append(reaction_time)
                    score += 1
                    circle_visible = False
                    next_circle_time = now + random.uniform(0.5, 1.5)

        if time_limit and (now - game_start_time) > time_limit:
            running = False
        if total_clicks and score >= total_clicks:
            running = False

        if circle_visible:
            pygame.draw.circle(screen, RED, circle_pos, radius)

        color_text = WHITE if sum(bg_color)/3 < 128 else BLACK
        draw_text(f"Score: {score}", 10, 10, color=color_text)
        if total_clicks:
            draw_text(f"Target: {score}/{total_clicks}", 10, 40, color=color_text)
        elif time_limit:
            remaining = int(time_limit - (now - game_start_time))
            draw_text(f"Time Left: {remaining}s", 10, 40, color=color_text)

        show_best_scores(bg_color)

        pygame.display.flip()
        clock.tick(60)

    if reaction_times:
        avg_time = sum(reaction_times) / len(reaction_times)
        if (best_reaction is None) or (avg_time < best_reaction):
            best_reaction = avg_time

        screen.fill(bg_color)
        draw_text(f"Average Reaction Time: {int(avg_time)} ms", width // 2, height // 2, center=True, color=color_text)
        show_best_scores(bg_color)
        pygame.display.flip()
        pygame.time.wait(3000)

def main_menu():
    dark_mode = True
    bg_color = DARK_BG if dark_mode else LIGHT_BG

    while True:
        screen.fill(bg_color)
        color_text = WHITE if sum(bg_color)/3 < 128 else BLACK
        draw_text("Welcome!", width // 2, 80, center=True, color=color_text)
        options = [
            "Aim Game",
            "Typing Game",
            f"Theme ({'Dark' if dark_mode else 'Light'})",
            "Quit"
        ]
        buttons = []
        for i, opt in enumerate(options):
            rect = draw_text(opt, width // 2, 180 + i * 60, center=True, color=color_text)
            buttons.append((rect, opt))

        show_best_scores(bg_color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for rect, val in buttons:
                    if rect.collidepoint((mx, my)):
                        if val == "Quit":
                            pygame.quit()
                            exit()
                        elif val.startswith("Theme"):
                            dark_mode = not dark_mode
                            bg_color = DARK_BG if dark_mode else LIGHT_BG
                        elif val == "Typing Game":
                            typing_trainer(bg_color)
                        elif val == "Aim Game":
                            run_reaction_game(bg_color)
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
