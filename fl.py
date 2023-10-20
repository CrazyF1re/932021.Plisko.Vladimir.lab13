from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def main_page():
    return render_template('/home.html')

@app.route("/Mockups")
def mockups():
    return render_template('./mockups.html')

if __name__ == "__main__":
    app.run( debug=True, port=80)
    