from flask import Flask,render_template,request, session, Blueprint, redirect, url_for, request
import sys,datetime,json
import flask_login

users = {'tommy': {'password': 'pass'},'mack':{'password':'word'}}


app = Flask(__name__)
app.secret_key = "secretKey"

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user




loggedIn = False

openIssues = []
closedIssues = []


@app.route("/")
def index():
    if loggedIn:
        print("not Logged in")
        return render_template('not-logged-in.html')
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
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form['user']
    if request.form["password"] == users[email]["password"]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected')) 
    
    
    
    return render_template('login.html', error=error)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route("/issue-tracker",methods=['GET','POST'])#get well, gets and post sends
@flask_login.login_required
def addOrRemoveIssue():
    def updatePage():
        print("RAN UPDATE")
        
        return render_template("issue-tracker.html",issueList=openIssues,closeIssueList=closedIssues)

    def addIssue():
        print("test2")
        issueName = request.form.get("issueName")
        issueDescription = request.form.get("issueDescription")
        assignee = request.form.get("assignee")
        #print(issueName,issueDescription,assignee)

        openIssueFiles = open("openIssues.txt","a+")


        if issueName == "" or issueDescription == "" or assignee == "":
            
            return render_template("issue-tracker.html",errorMessage = "Error: Not all values submitted!")
        date_object = datetime.date.today()
        try:
            issueFormat = "Name: "+ issueName + "\n" + "Description: " + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object)
        except:
            pass
        print("o")
        openIssues.append(issueFormat)
        openIssueFiles.write(issueFormat)


        #print(openIssues)
        return render_template("issue-tracker.html",issueList=openIssues,closeIssueList=closedIssues)
    def closeIssue():
        
        currentIssue = request.form.get("openIssueListItem")
        
        currentIssue = currentIssue.encode("ascii").decode("utf-8")
        currentIssue = currentIssue.replace("\r","")
        currentIssueLis = []
        

        splitLis = currentIssue.split()

        print(splitLis[len(splitLis) - 1])
        print(splitLis[len(splitLis) - 2])
        
        

        

        print(splitLis)
        currentIssueLis.append(currentIssue)

        print(currentIssueLis)
       





        if currentIssue in openIssues:
            print("IN OPEN ISSUES")
            spotInList = openIssues.index(currentIssue)
            print("spot in list: ",spotInList)
            openIssues.remove(currentIssue)
            closedIssues.append(currentIssue)
       
        print("\n")
        print("CURRENT ISSUES:",openIssues)
        print("CLOSED ISSUES:",closedIssues)
        print("\n")
      
        
        print("issueClosed")
        return render_template("issue-tracker.html",issueList=openIssues,closeIssueList = closedIssues)
        


    print(request.method)
    if request.method == "POST":
        createIssueButton = request.form.get("create-issue")
        closeIssueButton = request.form.get("close-issue-button")    
        
        
        if createIssueButton == "add":
            return addIssue()
    

    
        elif closeIssueButton == "close-issue":
            return closeIssue()

    else:
        return updatePage()

if __name__ == "__main__":
    app.run(debug=True)