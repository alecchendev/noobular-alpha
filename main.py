from flask import Flask, render_template

app = Flask(__name__)

counter = 0


@app.route("/")
def index() -> str:
    return render_template("index.html", counter=counter)


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    app.run(debug=True)
