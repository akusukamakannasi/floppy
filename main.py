import pygame
import sys
import random
import os
import asyncio  # Library wajib untuk kompatibilitas Web / Pygbag

# 1. Inisialisasi Pygame & Mixer Audio
pygame.init()
pygame.mixer.init()

# Ukuran Layar 16:9 (1280x720) dengan Scaling Otomatis
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Floppy Bird")

clock = pygame.time.Clock()

# 2. Memuat Aset Gambar (dengan fallback jika file tidak ditemukan)
try:
    bg_img = pygame.image.load("bg.png").convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception:
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((135, 206, 235))

try:
    bird_img = pygame.image.load("burung.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (60, 45))
except Exception:
    bird_img = pygame.Surface((60, 45))
    bird_img.fill((255, 255, 0))

try:
    pipe_img = pygame.image.load("pipa.png").convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (80, 500))
except Exception:
    pipe_img = pygame.Surface((80, 500))
    pipe_img.fill((0, 200, 0))

# 3. Memuat Aset Suara (.ogg untuk Web)
try:
    sound_jump = pygame.mixer.Sound("lompat.ogg")
    sound_score = pygame.mixer.Sound("skor.ogg")
    sound_hit = pygame.mixer.Sound("tabrak.ogg")
except Exception:
    sound_jump = sound_score = sound_hit = None

def play_sound(sound):
    if sound:
        sound.play()

# 4. Fungsi Manajemen High Score
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

# Setup Font
font_large = pygame.font.SysFont("Arial", 60, bold=True)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 28)

# 5. FUNGSI UTAMA ASYNC
async def main():
    high_score = load_highscore()
    
    # State Game: 'MENU', 'PLAYING', 'GAMEOVER'
    state = 'MENU'

    # Variabel Burung
    bird_x = 200
    bird_y = SCREEN_HEIGHT // 2
    bird_vy = 0
    gravity = 0.6
    jump_strength = -11

    # Variabel Pipa
    pipes = []
    pipe_gap = 210
    pipe_frequency = 1500  # milidetik
    last_pipe_time = pygame.time.get_ticks()

    score = 0
    
    # Animasi melayang di menu utama
    title_hover = 0
    title_hover_dir = 1

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # --- A. HANDLER INPUT / EVENT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_SPACE:
                    if state == 'MENU' or state == 'GAMEOVER':
                        state = 'PLAYING'
                        bird_y = SCREEN_HEIGHT // 2
                        bird_vy = jump_strength
                        pipes.clear()
                        score = 0
                        play_sound(sound_jump)
                    elif state == 'PLAYING':
                        bird_vy = jump_strength
                        play_sound(sound_jump)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Klik Kiri / Touch layaknya sentuhan HP
                    if state == 'MENU' or state == 'GAMEOVER':
                        state = 'PLAYING'
                        bird_y = SCREEN_HEIGHT // 2
                        bird_vy = jump_strength
                        pipes.clear()
                        score = 0
                        play_sound(sound_jump)
                    elif state == 'PLAYING':
                        bird_vy = jump_strength
                        play_sound(sound_jump)

        # --- B. LOGIKA PERMAINAN ---
        if state == 'MENU':
            title_hover += 0.5 * title_hover_dir
            if abs(title_hover) > 15:
                title_hover_dir *= -1

        elif state == 'PLAYING':
            bird_vy += gravity
            bird_y += bird_vy

            # Kemunculan Pipa Baru
            if current_time - last_pipe_time > pipe_frequency:
                top_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
                pipes.append({
                    'x': SCREEN_WIDTH,
                    'top_height': top_height,
                    'bottom_y': top_height + pipe_gap,
                    'passed': False
                })
                last_pipe_time = current_time

            # Pergerakan Pipa & Cek Skor
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

            # Deteksi Tabrakan (Atap/Lantai)
            bird_rect = pygame.Rect(bird_x, bird_y, 50, 35)
            if bird_y <= 0 or bird_y + 45 >= SCREEN_HEIGHT:
                play_sound(sound_hit)
                state = 'GAMEOVER'

            # Deteksi Tabrakan dengan Pipa
            for p in pipes:
                top_pipe_rect = pygame.Rect(p['x'], 0, 80, p['top_height'])
                bottom_pipe_rect = pygame.Rect(p['x'], p['bottom_y'], 80, SCREEN_HEIGHT - p['bottom_y'])

                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                    play_sound(sound_hit)
                    state = 'GAMEOVER'

        # --- C. PROSES RENDER GAMBAR ---
        screen.blit(bg_img, (0, 0))

        if state == 'MENU':
            title_surf = font_large.render("FLOPPY BIRD", True, (255, 255, 255))
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 180))

            bird_menu_y = 270 + title_hover
            screen.blit(bird_img, (SCREEN_WIDTH // 2 - 30, bird_menu_y))

            start_bg = pygame.Rect(SCREEN_WIDTH // 2 - 140, 400, 280, 70)
            pygame.draw.rect(screen, (230, 126, 34), start_bg, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), start_bg, 4, border_radius=15)

            start_text = font_medium.render("START GAME", True, (255, 255, 255))
            screen.blit(start_text, (start_bg.centerx - start_text.get_width() // 2, start_bg.centery - start_text.get_height() // 2))

            prompt_text = font_small.render("Tekan SPASI atau Sentuh Layar untuk Mulai", True, (240, 240, 240))
            screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 500))

            hs_text = font_small.render(f"High Score: {high_score}", True, (255, 215, 0))
            screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 560))

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

            score_surf = font_large.render(str(score), True, (255, 255, 255))
            screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 50))

            if state == 'GAMEOVER':
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                screen.blit(overlay, (0, 0))

                go_surf = font_large.render("GAME OVER", True, (231, 76, 60))
                screen.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, 220))

                score_info = font_medium.render(f"Skor: {score}   |   Tertinggi: {high_score}", True, (255, 255, 255))
                screen.blit(score_info, (SCREEN_WIDTH // 2 - score_info.get_width() // 2, 320))

                restart_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, 420, 300, 65)
                pygame.draw.rect(screen, (46, 204, 113), restart_btn, border_radius=15)
                pygame.draw.rect(screen, (255, 255, 255), restart_btn, 4, border_radius=15)

                restart_text = font_medium.render("MAIN LAGI", True, (255, 255, 255))
                screen.blit(restart_text, (restart_btn.centerx - restart_text.get_width() // 2, restart_btn.centery - restart_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)

        # Baris paling penting agar browser tidak freeze/unresponsive:
        await asyncio.sleep(0)

    pygame.quit()

# Eksekusi Async Loop
asyncio.run(main())