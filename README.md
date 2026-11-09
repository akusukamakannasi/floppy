# 🐤 Floppy Bird (Python & Pygame)

Sebuah game **Floppy Bird** yang dibangun menggunakan **Python** dan *library* **Pygame**. Game ini dilengkapi dengan antarmuka *fullscreen* beresio 16:9, fitur menu awal bergaya retro, efek suara, serta sistem *High Score* otomatis.

![Floppy Bird Preview](bg.png)

---

## 🚀 Fitur Utama

- **Tampilan Fullscreen 16:9**: Disesuaikan secara fleksibel menggunakan `pygame.SCALED` agar tajam di berbagai ukuran monitor.
- **Menu Utama Retro**: Dilengkapi tombol **START** interaktif dan animasi burung melayang di layar judul.
- **Kontrol Dual (Desktop & Sentuh)**:
  - Tombol `Spasi` atau **Klik Kiri Mouse** (Tap to Jump) untuk melompat.
  - Tombol `ESC` untuk keluar dari layar penuh secara langsung.
- **Sistem High Score**: Rekor skor tertinggi akan tersimpan secara otomatis di file `highscore.txt`.
- **Audio & Efek Suara**: Responsif terhadap aksi lompat, penambahan skor, dan saat terjadi benturan/kalah.
- **Fisika & Visual**: Dilengkapi efek rotasi burung yang dinamis sesuai dengan arah jatuh/kecepatan.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python 3.x
- **Library Game**: [Pygame](https://www.pygame.org/)
- **Packaging/Exe**: PyInstaller

---

## 🎮 Cara Menjalankan Game (Source Code)

### 1. Prasyarat
Pastikan Python 3 sudah terinstal di perangkatmu.

### 2. Kloning Repositori
```bash
git clone [https://github.com/akusukamakannasi/floppy.git](https://github.com/akusukamakannasi/floppy.git)
cd floppy
