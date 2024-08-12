import pygame
import random
import time
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Training Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND = (217,148,73)
TIME =  (132,242,179)
CROSS = (74,80,142)
MENU_COLOR = (191,57,62)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

SETTINGS_FILE = 'crosshair_settings.json'

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
            if 'color' not in settings:
                settings['color'] = list(CROSS)
            if 'line_length' not in settings:
                settings['line_length'] = 20
            if 'line_thickness' not in settings:
                settings['line_thickness'] = 2
            if 'gap' not in settings:
                settings['gap'] = 10
    except FileNotFoundError:
        settings = {
            'color': list(CROSS),
            'line_length': 20,
            'line_thickness': 2,
            'gap': 10
        }
    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)

def show_menu():
    screen.fill(MENU_COLOR)
    title_text = font.render("Aim Training Game", True, BLACK)
    start_text = small_font.render("1. Oyun Oyna", True, BLACK)
    settings_text = small_font.render("2. Ayarlar", True, BLACK)
    exit_text = small_font.render("3. Çıkış", True, BLACK)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def show_settings():
    settings = load_settings()

    while True:
        screen.fill(MENU_COLOR)
        title_text = font.render("Crosshair Settings", True, BLACK)
        color_text = small_font.render(f"1. Color: {settings['color']}", True, BLACK)
        line_length_text = small_font.render(f"2. Line Length: {settings['line_length']}", True, BLACK)
        line_thickness_text = small_font.render(f"3. Line Thickness: {settings['line_thickness']}", True, BLACK)
        gap_text = small_font.render(f"4. Gap: {settings['gap']}", True, BLACK)
        save_text = small_font.render("Press S to Save, D to Cancel", True, BLACK)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(line_length_text, (WIDTH // 2 - line_length_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(line_thickness_text, (WIDTH // 2 - line_thickness_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(gap_text, (WIDTH // 2 - gap_text.get_width() // 2, HEIGHT // 2 + 30))
        screen.blit(save_text, (WIDTH // 2 - save_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings['color'] = [(settings['color'][0] + 20) % 256, (settings['color'][1] + 20) % 256, (settings['color'][2] + 20) % 256]
                elif event.key == pygame.K_2:
                    settings['line_length'] = min(settings['line_length'] + 10, 100)
                elif event.key == pygame.K_3:
                    settings['line_thickness'] = min(settings['line_thickness'] + 1, 10)
                elif event.key == pygame.K_4:
                    settings['gap'] = min(settings['gap'] + 5, 50)

                elif event.key == pygame.K_d:
                    show_menu()
                    return
                elif event.key == pygame.K_s:
                    save_settings(settings)
                    return
             
def game_loop(crosshair_settings):
    pygame.mouse.set_visible(False)

    start_time = time.time()
    # total_time = 30  # 30 saniyelik süre
    total_time = 5  # 5 saniyelik süre // DEBUG
    crosshair_img = pygame.Surface((20, 20), pygame.SRCALPHA)
    crosshair_img.fill((0, 0, 0, 0))
    pygame.draw.line(crosshair_img, crosshair_settings['color'], 
                     (10 - crosshair_settings['line_length'] // 2, 10),
                     (10 + crosshair_settings['line_length'] // 2, 10),
                     crosshair_settings['line_thickness'])
    pygame.draw.line(crosshair_img, crosshair_settings['color'], 
                     (10, 10 - crosshair_settings['line_length'] // 2),
                     (10, 10 + crosshair_settings['line_length'] // 2),
                     crosshair_settings['line_thickness'])
    crosshair_rect = crosshair_img.get_rect()

    target_size = 30
    targets = []
    target_colors = []
    for _ in range(5):
        x = random.randint(0, WIDTH - target_size)
        y = random.randint(0, HEIGHT - target_size)
        color = random.choice([RED, GREEN, BLUE])
        targets.append(pygame.Rect(x, y, target_size, target_size))
        target_colors.append(color)

    score = 0
    running = True
    while running:
        screen.fill(BLACK)
        elapsed_time = time.time() - start_time
        remaining_time = total_time - int(elapsed_time)
        if remaining_time <= 0:
            running = False
        timer_text = font.render(str(remaining_time), True, TIME)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect.center = (mouse_x, mouse_y)

        for i, target in enumerate(targets):
            target.x += random.randint(-3, 3)
            target.y += random.randint(-3, 3)
            if target.left < 0 or target.right > WIDTH:
                target.x = random.randint(0, WIDTH - target_size)
            if target.top < 0 or target.bottom > HEIGHT:
                target.y = random.randint(0, HEIGHT - target_size)
            pygame.draw.rect(screen, target_colors[i], target)

        screen.blit(crosshair_img, crosshair_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, target in enumerate(targets):
                        if crosshair_rect.colliderect(target):
                            score += 1
                            targets.pop(i)
                            target_colors.pop(i)
                            x = random.randint(0, WIDTH - target_size)
                            y = random.randint(0, HEIGHT - target_size)
                            color = random.choice([RED, GREEN, BLUE])
                            new_target = pygame.Rect(x, y, target_size, target_size)
                            targets.append(new_target)
                            target_colors.append(color)
                            break

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return score

def main():
    crosshair_settings = load_settings()

    while True:
        show_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        score = game_loop(crosshair_settings)
                        break
                    elif event.key == pygame.K_2:
                        show_settings()
                        crosshair_settings = load_settings()
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        return
            else:
                continue
            break

        screen.fill(MENU_COLOR)
        result_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))
        retry_text = small_font.render("Press 1 to Play Again, 3 to Exit", True, BLACK)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 60))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        break
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        return
            else:
                continue
            break

if __name__ == "__main__":
    main()
