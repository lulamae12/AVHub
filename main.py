from flask import Flask,render_template,request, session, Blueprint, redirect, url_for, request
import sys,datetime
import json as jsonLib
import flask_login
from flask_socketio import SocketIO

from termcolor import colored
from flask_basicauth import BasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'avhub'
app.config['BASIC_AUTH_PASSWORD'] = 'barbarossa'

basic_auth = BasicAuth(app)

socket = SocketIO(app)


loggedIn = False

openIssues = []
closedIssues = []
chatList = []

@app.route("/authtest")

def secretVeiw():
    return render_template("issue-tracker.html")



@app.route("/")
def index():
    return render_template("home.html")


@app.route("/about")
def about():

    if request.method == "POST":
        print(request.form)
        print('hi')
    return render_template("about.html")
    

@app.route("/aboutButton")
def test():
    
    print("hello")
    
    
    return render_template("about.html")

@app.route("/home")
def home():
    
    return render_template("home.html")

@app.route("/track-hub")
def trackHub():
    return render_template("build-team-hub.html")

@app.route("/annex-image")
def annexImage():
    return render_template("annex-picture.html")




@app.route("/issue-tracker",methods=['GET','POST'])#get well, gets and post sends

def addOrRemoveIssue():
    def updatePage():
        print("RAN UPDATE")
        openIssueFile =  open("currentIssues.txt","r")

        for line in openIssueFile.readlines():
            
            # issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object) + "\n\n" + "This issue was logged by: " + creator
            line = line.replace("'","\"")
            issueData = json.loads(line)
            severityButton = issueData["IssueSeverityLevel"]
            issueName = issueData["Name"]
            issueDescription = issueData["Description"]
            assignee = issueData["AssignedTo"]
            date = issueData["DateCreated"]
            creator = issueData["Creator"]


            issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +date + "\n\n" + "This issue was logged by: " + creator
            
            if issueFormat not in openIssues:

                openIssues.append(issueFormat)
        return render_template("issue-tracker.html",issueList=openIssues,closeIssueList=closedIssues)

    def addIssue():
        print("test2")
        issueName = request.form.get("issueName")
        issueDescription = request.form.get("issueDescription")
        assignee = request.form.get("assignee")
        creator = request.form.get("creator")
        severityButton = request.form.get("exampleRadios")

        #print(issueName,issueDescription,assignee)

        



        if issueName == "" or issueDescription == "" or assignee == "":
          
            return render_template("issue-tracker.html",errorMessage = "Error: Not all values submitted!")
        date_object = datetime.date.today()
        try:
            issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object) + "\n\n" + "This issue was logged by: " + creator
        except:
            pass
        
        jsonDataToWrite = {
                    "IssueSeverityLevel":severityButton,
                    "Name":issueName,
                    "Description":issueDescription,
                    "AssignedTo":assignee,
                    "DateCreated":str(date_object),
                    "Creator":creator
                    }
        openIssueFile =  open("currentIssues.txt","a+")
    

        openIssueFile.write(str(jsonDataToWrite))
        openIssueFile.write("\n")
        openIssueFile.close()

        openIssueFile =  open("currentIssues.txt","r")

        for line in openIssueFile.readlines():
            
            # issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object) + "\n\n" + "This issue was logged by: " + creator
            line = line.replace("'","\"")
            issueData = json.loads(line)
            severityButton = issueData["IssueSeverityLevel"]
            issueName = issueData["Name"]
            issueDescription = issueData["Description"]
            assignee = issueData["AssignedTo"]
            date = issueData["DateCreated"]
            creator = issueData["Creator"]


            issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +date + "\n\n" + "This issue was logged by: " + creator
            






            if issueFormat not in openIssues:

                openIssues.append(issueFormat)
            



        print("o")
        
        

        

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
      
        closedIssuesFile = open("closedIssues.txt","a+")
        for item in range(len(closedIssues)):
            closedIssuesFile.write(closedIssues[item])
        
        
        




        
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




    
@app.route('/chat')
def chat():
    return render_template('chat.html')

def messageReceived(methods=['GET', 'POST']):
    print('message received')

@socket.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socket.emit('my response', json, callback=messageReceived)
    chatLog = open("chatLog.txt","a+")
    chatLog.write(str(json))
    chatLog.write("\n")
    chatLog.close()














if __name__ == "__main__":
    
    app.run(debug=True)