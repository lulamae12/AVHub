from flask import Flask,render_template,request, redirect, url_for, request
import sys

app = Flask(__name__)

loggedIn = False



@app.route("/")
def index():
    if loggedIn:
        return "you are at the index"
    else:
        return render_template("not-logged-in.html")
        

@app.route("/about")
def about():
    if loggedIn:
        if request.method == "POST":
            print(request.form)
            print('hi')
        return render_template("about.html")
    else:
        return render_template("not-logged-in.html")

@app.route("/aboutButton")
def test():
    if loggedIn:
        print("hello")
    
    
        return render_template("about.html")
    else:
        return render_template("not-logged-in.html")

@app.route("/home")
def home():
    if loggedIn:
        return render_template("home.html")
    else:
        return render_template("not-logged-in.html")
@app.route("/login",methods=['GET','POST'])
def login():
    
    error = None
    if request.method == 'POST':
        if request.form['user'] != 'admin' or request.form["password"] != "admin":
            error = 'Invalid Credentials. Please try again.'
            print("user: ",request.form.get('user'))
            print("password: ",request.form.get('password'))
            print("error")
        else:
            global loggedIn
            loggedIn = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
    
    
    return render_template("login.html")


@app.route("/issue-tracker")
def issueTracker():
    if loggedIn:
        return render_template("issue-tracker.html")    
    else:
        return render_template("not-logged-in.html")
if __name__ == "__main__":
    app.run(debug=True)