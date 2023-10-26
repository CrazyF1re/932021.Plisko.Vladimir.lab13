from flask import Flask, render_template,request,g,make_response
import sqlite3
import os

app = Flask(__name__)
DATABASE = f"{os.path.join(app.root_path,'flsite.db')}"
app.config.from_object(__name__)
id = 1


@app.route("/")
def main_page():
    global id
    if request.cookies.get('id')==None:
        resp = make_response(render_template('/home.html'))
        resp.set_cookie('id',f"{id}")
        id += 1
        return resp
    else:
        return render_template('/home.html')

@app.route("/Mockups")
def mockups():
    return render_template('./mockups.html')

@app.route("/Mockups/Quiz", methods = ["POST","GET"])
def addvalue():
    if request.method == "POST":
        answer = request.form.get('answer')
        example = request.form.get('example')[:-1]
        db = get_db()
        db.cursor().execute("""INSERT INTO quiz(id,example,answer,correct) values(?,?,?,?)""", (request.cookies.get('id'),example,answer,eval(example)==int(answer)))
        db.commit()
        db.close()
        return render_template('./quiz.html')
    if request.method == "GET":
        if request.args.get('type') == 'quiz':
            return render_template("./quiz.html")
        else:
            db = get_db()
            return render_template("./results.html",
                answers = db.cursor().execute("""SELECT example,answer from quiz where id=?""",(request.cookies.get('id'),)).fetchall(),
                right_answers = db.cursor().execute("""SELECT sum(correct) from quiz where id=?""",(request.cookies.get('id'),)).fetchone(),
                all_answers = db.cursor().execute("""SELECT count(correct) from quiz where id=?""",(request.cookies.get('id'),)).fetchone())
    
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()



def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql','r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close() 

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

if __name__ == "__main__":
    create_db()
    app.run( debug=True, port=80)
    
    