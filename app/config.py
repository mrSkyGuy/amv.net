from secrets import token_hex

HOST, PORT = "127.0.0.1", "8080"
SECRET_KEY = token_hex(16)
