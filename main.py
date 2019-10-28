from flask import Flask,render_template,request, redirect, url_for, request
import sys,datetime,json
app = Flask(__name__)

loggedIn = False

openIssues = []
closedIssues = []

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





@app.route("/issue-tracker",methods=['GET','POST'])#get well, gets and post sends
def addOrRemoveIssue():
    def updatePage():
        print("RAN UPDATE")
        
        return render_template("issue-tracker.html",issueList=openIssues)

    def addIssue():
        print("test2")
        issueName = request.form.get("issueName")
        issueDescription = request.form.get("issueDescription")
        assignee = request.form.get("assignee")
        print(issueName,issueDescription,assignee)



        if issueName == "" or issueDescription == "" or assignee == "":
            
            return render_template("issue-tracker.html",errorMessage = "Error: Not all values submitted!")
        date_object = datetime.date.today()
        try:
            issueFormat = "Name: "+ issueName + "\n" + "Description: " + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object)
        except:
            pass

        openIssues.append(issueFormat)
        print(openIssues)
        return render_template("issue-tracker.html",issueList=openIssues)

    if request.method == "POST":
        if request.form["create-issue"] == "add":
            return addIssue()
    else:
        return updatePage()

if __name__ == "__main__":
    app.run(debug=True)