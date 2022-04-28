from secrets import token_hex

HOST, PORT = "127.0.0.1", "8080"
SECRET_KEY = token_hex(16)
DEBUG_MODE = False
MAX_CONTENT_LENGTH = 30 * 2 ** 20  # 15 MB
UPLOAD_EXTENSIONS = [".jpg", ".png", ".jpeg", ".mp4", ".webm", ".ogv"]
