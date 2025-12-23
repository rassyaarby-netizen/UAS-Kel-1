import webbrowser

# Konfigurasi Level
LEVEL_NAME = "MEDIUM"
TIME_LIMIT = 15  # Detik
COLOR = (225, 255, 0) # Hijau

def punishment():
    youtube_url = "https://youtu.be/xvFZjo5PgG0"
    print("Hukuman: Membuka YouTube...")
    try:
        webbrowser.open_new_tab(youtube_url)
    except Exception as e:
        print("Gagal membuka browser:", e)