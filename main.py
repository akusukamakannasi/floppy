import pygame
import sys
import random
import os
import asyncio

# 1. Inisialisasi Pygame & Sound
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Floppy Bird 8-Bit")

clock = pygame.time.Clock()

# 2. Sistem Font Pixel Retro
def get_pixel_font(size):
    try:
        return pygame.font.Font("PressStart2P.ttf", size)
    except Exception:
        return pygame.font.SysFont("Courier", int(size * 1.1), bold=True)

font_title = get_pixel_font(48)
font_medium = get_pixel_font(24)
font_small = get_pixel_font(18)

# 3. Memuat Aset Gambar & Suara
try:
    bg_img = pygame.image.load("bg.png").convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception:
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((74, 155, 222))

try:
    bird_img = pygame.image.load("burung.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (60, 45))
except Exception:
    bird_img = pygame.Surface((60, 45))
    bird_img.fill((248, 216, 0))

try:
    pipe_img = pygame.image.load("pipa.png").convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (80, 500))
except Exception:
    pipe_img = pygame.Surface((80, 500))
    pipe_img.fill((0, 200, 0))

try:
    sound_jump = pygame.mixer.Sound("lompat.ogg")
    sound_score = pygame.mixer.Sound("skor.ogg")
    sound_hit = pygame.mixer.Sound("tabrak.ogg")
except Exception:
    sound_jump = sound_score = sound_hit = None

def play_sound(sound):
    if sound:
        sound.play()

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass

# 4. Helper Render Teks & Panel Retro 8-Bit
def draw_pixel_text(surface, text, font, color, shadow_color, center_x, center_y):
    shadow_surf = font.render(text, False, shadow_color)
    shadow_rect = shadow_surf.get_rect(center=(center_x + 4, center_y + 4))
    surface.blit(shadow_surf, shadow_rect)

    main_surf = font.render(text, False, color)
    main_rect = main_surf.get_rect(center=(center_x, center_y))
    surface.blit(main_surf, main_rect)

def draw_retro_box(surface, rect, fill_color, border_color, outer_border_color):
    pygame.draw.rect(surface, outer_border_color, rect.inflate(12, 12))
    pygame.draw.rect(surface, border_color, rect.inflate(6, 6))
    pygame.draw.rect(surface, fill_color, rect)

# 5. FUNGSI UTAMA GAME
async def main():
    high_score = load_highscore()
    state = 'MENU'

    bird_x = 200
    bird_y = SCREEN_HEIGHT // 2
    bird_vy = 0
    gravity = 0.6
    jump_strength = -11

    pipes = []
    pipe_gap = 210
    pipe_frequency = 1500
    last_pipe_time = pygame.time.get_ticks()

    score = 0
    title_hover = 0
    title_hover_dir = 1

    # Area tombol presisi
    start_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 160, 370, 320, 64)
    restart_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 56)

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_SPACE:
                    if state == 'MENU':
                        state = 'PLAYING'
                        bird_y = SCREEN_HEIGHT // 2
                        bird_vy = jump_strength
                        pipes.clear()
                        score = 0
                        play_sound(sound_jump)
                    elif state == 'GAMEOVER':
                        state = 'MENU'
                    elif state == 'PLAYING':
                        bird_vy = jump_strength
                        play_sound(sound_jump)

            # Kontrol Sentuh / Klik Tombol Presisi
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_pos = event.pos

                    if state == 'MENU':
                        # Hanya mulai jika menekan tombol START GAME
                        if start_btn_rect.collidepoint(click_pos):
                            state = 'PLAYING'
                            bird_y = SCREEN_HEIGHT // 2
                            bird_vy = jump_strength
                            pipes.clear()
                            score = 0
                            play_sound(sound_jump)

                    elif state == 'GAMEOVER':
                        # Hanya kembali ke MENU jika menekan tombol MAIN LAGI
                        if restart_btn_rect.collidepoint(click_pos):
                            state = 'MENU'

                    elif state == 'PLAYING':
                        bird_vy = jump_strength
                        play_sound(sound_jump)

        if state == 'MENU':
            title_hover += 0.4 * title_hover_dir
            if abs(title_hover) > 12:
                title_hover_dir *= -1

        elif state == 'PLAYING':
            bird_vy += gravity
            bird_y += bird_vy

            if current_time - last_pipe_time > pipe_frequency:
                top_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
                pipes.append({
                    'x': SCREEN_WIDTH,
                    'top_height': top_height,
                    'bottom_y': top_height + pipe_gap,
                    'passed': False
                })
                last_pipe_time = current_time

            for p in pipes:
                p['x'] -= 5
                if not p['passed'] and p['x'] + 80 < bird_x:
                    p['passed'] = True
                    score += 1
                    if score > high_score:
                        high_score = score
                        save_highscore(high_score)
                    play_sound(sound_score)

            pipes = [p for p in pipes if p['x'] > -100]

            bird_rect = pygame.Rect(bird_x, bird_y, 50, 35)
            if bird_y <= 0 or bird_y + 45 >= SCREEN_HEIGHT:
                play_sound(sound_hit)
                state = 'GAMEOVER'

            for p in pipes:
                top_pipe_rect = pygame.Rect(p['x'], 0, 80, p['top_height'])
                bottom_pipe_rect = pygame.Rect(p['x'], p['bottom_y'], 80, SCREEN_HEIGHT - p['bottom_y'])

                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                    play_sound(sound_hit)
                    state = 'GAMEOVER'

        screen.blit(bg_img, (0, 0))

        if state == 'MENU':
            draw_pixel_text(screen, "FLOPPY BIRD", font_title, (248, 216, 0), (0, 0, 0), SCREEN_WIDTH // 2, 170)

            bird_menu_y = 260 + title_hover
            screen.blit(bird_img, (SCREEN_WIDTH // 2 - 30, bird_menu_y))

            draw_retro_box(screen, start_btn_rect, (230, 81, 0), (255, 183, 77), (0, 0, 0))
            draw_pixel_text(screen, "START GAME", font_medium, (255, 255, 255), (0, 0, 0), start_btn_rect.centerx, start_btn_rect.centery)

            hs_box = pygame.Rect(SCREEN_WIDTH // 2 - 160, 480, 320, 48)
            draw_retro_box(screen, hs_box, (33, 33, 33), (117, 117, 117), (0, 0, 0))
            draw_pixel_text(screen, f"HIGH SCORE: {high_score}", font_small, (248, 216, 0), (0, 0, 0), hs_box.centerx, hs_box.centery)

        elif state in ['PLAYING', 'GAMEOVER']:
            for p in pipes:
                top_pipe_scaled = pygame.transform.scale(pipe_img, (80, p['top_height']))
                top_pipe_flipped = pygame.transform.flip(top_pipe_scaled, False, True)
                screen.blit(top_pipe_flipped, (p['x'], 0))

                bottom_height = SCREEN_HEIGHT - p['bottom_y']
                bottom_pipe_scaled = pygame.transform.scale(pipe_img, (80, bottom_height))
                screen.blit(bottom_pipe_scaled, (p['x'], p['bottom_y']))

            angle = max(-30, min(30, -bird_vy * 3))
            rotated_bird = pygame.transform.rotate(bird_img, angle)
            screen.blit(rotated_bird, (bird_x, bird_y))

            draw_pixel_text(screen, str(score), font_title, (255, 255, 255), (0, 0, 0), SCREEN_WIDTH // 2, 70)

            if state == 'GAMEOVER':
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (0, 0))

                go_box = pygame.Rect(SCREEN_WIDTH // 2 - 220, 160, 440, 320)
                draw_retro_box(screen, go_box, (33, 33, 33), (224, 224, 224), (0, 0, 0))

                draw_pixel_text(screen, "GAME OVER", font_title, (229, 57, 53), (0, 0, 0), SCREEN_WIDTH // 2, 230)
                draw_pixel_text(screen, f"SKOR    : {score}", font_medium, (255, 255, 255), (0, 0, 0), SCREEN_WIDTH // 2, 300)
                draw_pixel_text(screen, f"TERTINGGI: {high_score}", font_medium, (248, 216, 0), (0, 0, 0), SCREEN_WIDTH // 2, 345)

                draw_retro_box(screen, restart_btn_rect, (67, 160, 71), (129, 199, 132), (0, 0, 0))
                draw_pixel_text(screen, "MAIN LAGI", font_medium, (255, 255, 255), (0, 0, 0), restart_btn_rect.centerx, restart_btn_rect.centery)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())