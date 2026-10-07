import base64
import hashlib
import json
import secrets
import urllib.parse
import webbrowser


CLIENT_ID = "54801756"
REDIRECT_URI = "https://logmax-vk-callback.onrender.com/"

OAUTH_STATE_FILE = "vk_oauth_state.json"


# Генерируем PKCE
code_verifier = secrets.token_urlsafe(64)

code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()

state = secrets.token_urlsafe(32)


# Сохраняем данные локально
with open(OAUTH_STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "code_verifier": code_verifier,
            "state": state,
        },
        f,
        ensure_ascii=False,
        indent=4,
    )


params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": state,
}

url = "https://id.vk.ru/authorize?" + urllib.parse.urlencode(params)


print("Открой эту ссылку в браузере:")
print()
print(url)
print()
print("Данные PKCE сохранены в:", OAUTH_STATE_FILE)
print()
print("State:")
print(state)


webbrowser.open(url)

