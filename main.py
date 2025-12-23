import pygame
import sys
import random
import easy
import medium
import hard

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudden Death Quiz - Pygame Edition")

# Warna & Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 153, 213)
RED = (200, 0, 0)
GREEN = (0, 180, 0)

font_besar = pygame.font.SysFont("Arial", 40, bold=True)
font_sedang = pygame.font.SysFont("Arial", 30)
font_kecil = pygame.font.SysFont("Arial", 22)

class QuizGame:
    def __init__(self):
        self.running = True
        self.reset_game_data()

    def reset_game_data(self):
        """Mereset semua data untuk permainan baru"""
        self.state = "INPUT_NAMA"
        self.module = None
        self.nama = ""
        self.skor = 0
        self.soal_index = 0
        self.sisa_waktu = 0
        self.last_tick = 0
        
        bank_soal = [
            {"p": "Ibukota Indonesia?", "o": ["A. Jakarta", "B. Bandung", "C. Surabaya", "D. Medan"], "j": "A"},
            {"p": "Planet terdekat dari Matahari?", "o": ["A. Venus", "B. Mars", "C. Merkurius", "D. Jupiter"], "j": "C"},
            {"p": "Penemu lampu pijar?", "o": ["A. Tesla", "B. Edison", "C. Einstein", "D. Bell"], "j": "B"},
            {"p": "5 + 7 x 2 = ?", "o": ["A. 24", "B. 17", "C. 19", "D. 22"], "j": "C"},
            {"p": "Samudra terbesar?", "o": ["A. Atlantik", "B. Hindia", "C. Arktik", "D. Pasifik"], "j": "D"},
            {"p": "Asal bela diri muay thai?", "o": ["A. Jerman", "B. Thailand", "C. Malaysia", "D. Indonesia"], "j": "B"},
            {"p": "Bahasa yang di gunakan negara brazil?", "o": ["A. Brazil", "B. Spanyol", "C. Portugis", "D. Inggris"], "j": "C"},
            {"p": "Berapa jumlah benua di dunia?", "o": ["A. 7", "B. 5", "C. 4", "D. 6"], "j": "A"},
            {"p": "Negara dengan penduduk terbanyak di dunia?", "o": ["A. Russia", "B. Amerika", "C. Indonesia", "D. China"], "j": "D"},
            {"p": "Negara terkecil di dunia?", "o": ["A. Singapura", "B. Vatikan", "C. Monaco", "D. Nauru"], "j": "B"},
        ]
        self.soal_terpilih = random.sample(bank_soal, 3)

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(text, True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        screen.blit(img, rect)

    def input_nama_screen(self):
        screen.fill(WHITE)
        self.draw_text("MASUKKAN NAMA ANDA", font_besar, BLACK, WIDTH//2, 150, True)
        input_rect = pygame.Rect(WIDTH//2 - 150, 250, 300, 50)
        pygame.draw.rect(screen, GRAY, input_rect, border_radius=5)
        pygame.draw.rect(screen, BLUE, input_rect, 2, border_radius=5)
        self.draw_text(self.nama, font_sedang, BLACK, WIDTH//2, 275, True)
        self.draw_text("Tekan ENTER untuk Lanjut", font_kecil, (100, 100, 100), WIDTH//2, 350, True)

    def menu_screen(self):
        screen.fill(WHITE)
        self.draw_text(f"HALO, {self.nama.upper()}!", font_sedang, BLUE, WIDTH//2, 50, True)
        self.draw_text("Pilih Tingkat Kesulitan:", font_sedang, BLACK, WIDTH//2, 180, True)
        options = [("1. MUDAH", GREEN, 250), ("2. SEDANG", (200, 200, 0), 320), ("3. SULIT", RED, 390)]
        for text, color, y in options:
            pygame.draw.rect(screen, color, (300, y, 200, 50), border_radius=10)
            self.draw_text(text, font_kecil, WHITE, WIDTH//2, y + 25, True)

    def play_screen(self):
        screen.fill(WHITE)
        soal = self.soal_terpilih[self.soal_index]
        pygame.draw.rect(screen, self.module.COLOR, (0, 0, WIDTH, 60))
        self.draw_text(f"Player: {self.nama}", font_kecil, BLACK, 20, 15)
        self.draw_text(f"Timer: {int(self.sisa_waktu)}s", font_kecil, BLACK, WIDTH-120, 15)
        self.draw_text(f"Soal {self.soal_index + 1}/3", font_sedang, BLUE, 50, 100)
        self.draw_text(soal['p'], font_sedang, BLACK, 50, 150)
        for i, opsi in enumerate(soal['o']):
            self.draw_text(opsi, font_kecil, BLACK, 70, 250 + (i * 45))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Opsi Exit Global (Tekan ESC kapan saja untuk keluar)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Logic Restart saat Win/Loss
                if self.state in ["WIN", "GAMEOVER"]:
                    if event.key == pygame.K_r:
                        self.reset_game_data()

                # Logic Input Nama
                elif self.state == "INPUT_NAMA":
                    if event.key == pygame.K_RETURN and self.nama.strip():
                        self.state = "MENU"
                    elif event.key == pygame.K_BACKSPACE:
                        self.nama = self.nama[:-1]
                    else:
                        if (event.unicode.isalpha() or event.unicode.isspace()) and len(self.nama) < 15:
                            self.nama += event.unicode

                # Logic Menu
                elif self.state == "MENU":
                    if event.key == pygame.K_1: self.start_game(easy)
                    elif event.key == pygame.K_2: self.start_game(medium)
                    elif event.key == pygame.K_3: self.start_game(hard)
                
                # Logic Play
                elif self.state == "PLAYING":
                    key_map = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D"}
                    if event.key in key_map:
                        self.check_answer(key_map[event.key])

    def start_game(self, mod):
        self.module = mod
        self.sisa_waktu = mod.TIME_LIMIT
        self.state = "PLAYING"
        self.last_tick = pygame.time.get_ticks()

    def check_answer(self, user_ans):
        if user_ans == self.soal_terpilih[self.soal_index]['j']:
            self.skor += 1
            self.soal_index += 1
            if self.soal_index >= 3: self.state = "WIN"
        else:
            self.trigger_punishment()

    def trigger_punishment(self):
        self.state = "GAMEOVER"
        self.module.punishment()

    def update(self):
        if self.state == "PLAYING":
            now = pygame.time.get_ticks()
            if now - self.last_tick >= 1000:
                self.sisa_waktu -= 1
                self.last_tick = now
            if self.sisa_waktu <= 0: self.trigger_punishment()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            
            if self.state == "INPUT_NAMA":
                self.input_nama_screen()
            elif self.state == "MENU":
                self.menu_screen()
            elif self.state == "PLAYING":
                self.play_screen()
            elif self.state == "GAMEOVER":
                screen.fill(RED)
                self.draw_text("GAME OVER", font_besar, WHITE, WIDTH//2, HEIGHT//2 - 60, True)
                self.draw_text("Tekan 'R' untuk Ulangi | Tekan 'ESC' untuk Keluar", font_kecil, WHITE, WIDTH//2, HEIGHT//2 + 40, True)
            elif self.state == "WIN":
                screen.fill(GREEN)
                self.draw_text(f"MENANG! SKOR: {self.skor}/3", font_besar, WHITE, WIDTH//2, HEIGHT//2 - 60, True)
                self.draw_text("Tekan 'R' untuk Main Lagi | Tekan 'ESC' untuk Keluar", font_kecil, WHITE, WIDTH//2, HEIGHT//2 + 40, True)

            pygame.display.flip()

if __name__ == "__main__":
    game = QuizGame()
    game.run()