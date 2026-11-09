import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# --- RESOLUSI FULLSCREEN 16:9 (1280 x 720) ---
LEBAR = 1280
TINGGI = 720
layar = pygame.display.set_mode((LEBAR, TINGGI), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Clone Flappy Bird Ultimate 16:9")
clock = pygame.time.Clock()

font_teks = pygame.font.Font(None, 45)
font_judul = pygame.font.Font(None, 75)
font_tombol = pygame.font.Font(None, 55)

# --- MEMUAT GAMBAR ---
gambar_bg = pygame.image.load("bg.png").convert_alpha()
gambar_bg = pygame.transform.scale(gambar_bg, (LEBAR, TINGGI))

gambar_burung = pygame.image.load("burung.png").convert_alpha()
gambar_burung = pygame.transform.scale(gambar_burung, (40, 40))
gambar_burung_menu = pygame.transform.scale(gambar_burung, (55, 55))

gambar_pipa = pygame.image.load("pipa.png").convert_alpha()

# --- MEMUAT AUDIO (Kebal Error) ---
try:
    suara_lompat = pygame.mixer.Sound("lompat.wav")
    suara_skor = pygame.mixer.Sound("skor.wav")
    suara_tabrak = pygame.mixer.Sound("tabrak.wav")
    audio_aktif = True
except:
    audio_aktif = False

# --- HIGH SCORE ---
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# --- VARIABEL GAME ---
burung_x = 150
burung_y = 360
burung_lebar = 40
burung_tinggi = 40
gravitasi = 0.5
kecepatan_y = 0
lompatan = -8.5

pipa_lebar = 70
pipa_x = LEBAR
pipa_gap = 180
tinggi_pipa_bawah = random.randint(150, 450)

# Status Game
tampilan_awal = True
game_aktif = False
skor = 0
skor_dihitung = False

# Tombol START Retro (Presisi Tengah Layar 16:9)
tombol_start_rect = pygame.Rect(LEBAR // 2 - 110, 500, 220, 70)

burung_berputar = gambar_burung 
pipa_atas_img = pygame.Surface((0,0))
pipa_bawah_img = pygame.Surface((0,0))

# --- GAME LOOP ---
while True:
    posisi_mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            if event.key == pygame.K_SPACE and game_aktif:
                kecepatan_y = lompatan 
                if audio_aktif: suara_lompat.play()

        # DETEKSI KLIK MOUSE / TAP DI MANA SAJA (KONTROL SENTUH MOBILE)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Jika di menu awal atau game over -> Cek tombol START
            if (tampilan_awal or not game_aktif) and tombol_start_rect.collidepoint(posisi_mouse):
                tampilan_awal = False
                game_aktif = True
                burung_y = 360
                kecepatan_y = 0
                pipa_x = LEBAR
                tinggi_pipa_bawah = random.randint(150, 450)
                skor = 0
                skor_dihitung = False
                if audio_aktif: suara_lompat.play()
            
            # Jika game sedang berjalan -> KLIK DI MANA SAJA UNTUK LOMPAT
            elif game_aktif:
                kecepatan_y = lompatan
                if audio_aktif: suara_lompat.play()

    layar.blit(gambar_bg, (0, 0))
    
    # 1. TAMPILAN MENU AWAL (RETRO 16:9)
    if tampilan_awal:
        teks_judul = font_judul.render("FLAPPY BIRD", True, (255, 255, 255))
        layar.blit(teks_judul, (440, 180))
        layar.blit(gambar_burung_menu, (810, 175))

        # Tombol START Retro
        warna_tombol = (245, 115, 35) if tombol_start_rect.collidepoint(posisi_mouse) else (220, 85, 20)
        pygame.draw.rect(layar, (60, 30, 10), tombol_start_rect, border_radius=6)
        pygame.draw.rect(layar, (255, 255, 255), tombol_start_rect.inflate(-6, -6), border_radius=4)
        pygame.draw.rect(layar, warna_tombol, tombol_start_rect.inflate(-14, -14), border_radius=2)
        
        teks_start = font_tombol.render("START", True, (255, 255, 255))
        layar.blit(teks_start, (tombol_start_rect.x + 43, tombol_start_rect.y + 16))

        teks_petunjuk = font_teks.render("Klik layar / Spasi untuk melompat", True, (255, 255, 255))
        layar.blit(teks_petunjuk, (390, 600))

    # 2. TAMPILAN GAME BERJALAN
    elif game_aktif:
        kecepatan_y += gravitasi  
        burung_y += kecepatan_y   
        kotak_burung = pygame.Rect(burung_x, burung_y, burung_lebar, burung_tinggi)
        
        rotasi = kecepatan_y * -3
        if rotasi > 30: rotasi = 30
        elif rotasi < -90: rotasi = -90
        burung_berputar = pygame.transform.rotozoom(gambar_burung, rotasi, 1)
        layar.blit(burung_berputar, kotak_burung)

        pipa_x -= 5 
        if pipa_x < -pipa_lebar:
            pipa_x = LEBAR
            tinggi_pipa_bawah = random.randint(150, 450)
            skor_dihitung = False

        tinggi_pipa_atas = TINGGI - tinggi_pipa_bawah - pipa_gap
        pipa_atas_rect = pygame.Rect(pipa_x, 0, pipa_lebar, tinggi_pipa_atas)
        pipa_bawah_rect = pygame.Rect(pipa_x, TINGGI - tinggi_pipa_bawah, pipa_lebar, tinggi_pipa_bawah)
        
        pipa_atas_img = pygame.transform.scale(gambar_pipa, (pipa_lebar, tinggi_pipa_atas))
        pipa_atas_img = pygame.transform.flip(pipa_atas_img, False, True)
        pipa_bawah_img = pygame.transform.scale(gambar_pipa, (pipa_lebar, tinggi_pipa_bawah))
        
        layar.blit(pipa_atas_img, pipa_atas_rect)
        layar.blit(pipa_bawah_img, pipa_bawah_rect)

        if burung_x > pipa_x + pipa_lebar and not skor_dihitung:
            skor += 1
            skor_dihitung = True
            if audio_aktif: suara_skor.play()

        if burung_y > TINGGI or burung_y < 0:
            game_aktif = False
            if audio_aktif: suara_tabrak.play()
            
        if kotak_burung.colliderect(pipa_atas_rect) or kotak_burung.colliderect(pipa_bawah_rect):
            game_aktif = False
            if audio_aktif: suara_tabrak.play()
            
        if skor > high_score:
            high_score = skor
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))
            
        teks_skor = font_teks.render(str(skor), True, (255, 255, 255))
        layar.blit(teks_skor, (LEBAR // 2, 50))
            
    # 3. TAMPILAN GAME OVER
    else:
        layar.blit(burung_berputar, kotak_burung)
        layar.blit(pipa_atas_img, pipa_atas_rect)
        layar.blit(pipa_bawah_img, pipa_bawah_rect)
        
        teks_gameover = font_teks.render("GAME OVER", True, (255, 0, 0))
        teks_skor_akhir = font_teks.render(f"Skor Saat Ini: {skor}", True, (255, 255, 255))
        teks_high_score = font_teks.render(f"Tertinggi: {high_score}", True, (255, 255, 0))
        
        layar.blit(teks_gameover, (540, 150))
        layar.blit(teks_skor_akhir, (520, 210))
        layar.blit(teks_high_score, (535, 260))
        
        # Tombol START Restart
        warna_tombol = (245, 115, 35) if tombol_start_rect.collidepoint(posisi_mouse) else (220, 85, 20)
        pygame.draw.rect(layar, (60, 30, 10), tombol_start_rect, border_radius=6)
        pygame.draw.rect(layar, (255, 255, 255), tombol_start_rect.inflate(-6, -6), border_radius=4)
        pygame.draw.rect(layar, warna_tombol, tombol_start_rect.inflate(-14, -14), border_radius=2)
        
        teks_start = font_tombol.render("START", True, (255, 255, 255))
        layar.blit(teks_start, (tombol_start_rect.x + 43, tombol_start_rect.y + 16))

        teks_petunjuk = font_teks.render("Tekan ESC untuk Keluar Game", True, (255, 255, 255))
        layar.blit(teks_petunjuk, (415, 600))

    pygame.display.update()
    clock.tick(60)