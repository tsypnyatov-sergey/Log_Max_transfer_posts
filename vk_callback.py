
from flask import Flask, request
import html

app = Flask(__name__)


@app.route("/")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        return f"""
        <h2>Ошибка VK</h2>
        <p>{html.escape(error)}</p>
        """

    if not code:
        return """
        <h2>VK OAuth callback</h2>
        <p>Код авторизации не получен.</p>
        """

    print("\n=== VK CALLBACK ===")
    print("CODE получен")
    print("STATE:", state)

    return """
    <h2>Авторизация VK получена</h2>
    <p>Код авторизации получен успешно.</p>
    <p>Это окно можно закрыть.</p>
    """


if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )

