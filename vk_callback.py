from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        return f"Ошибка VK: {error}"

    print("\n=== VK CALLBACK ===")
    print("CODE:", code)
    print("STATE:", state)

    return "Авторизация VK получена. Это окно можно закрыть."


if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )