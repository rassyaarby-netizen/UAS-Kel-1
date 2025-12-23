import webbrowser

# Konfigurasi Level
LEVEL_NAME = "HARD"
TIME_LIMIT = 7  # Detik
COLOR = (0, 0, 225) # Hijau

def punishment():
    youtube_url = "https://youtu.be/xvFZjo5PgG0"
    print("Hukuman: Membuka YouTube...")
    try:
        webbrowser.open_new_tab(youtube_url)
    except Exception as e:
        print("Gagal membuka browser:", e)