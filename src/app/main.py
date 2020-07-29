from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("instances.html")


if __name__ == "__main__":
    app.run("localhost", port=9191, debug=True)
