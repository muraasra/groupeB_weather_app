from flask import Flask,render_template # type: ignore
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home/home.html')	
if __name__ == "__main__":
    app.run(debug=True)


def main():
    print("Hello, world!")
    if __name__ == "__main__":
        main()