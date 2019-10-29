from flask import Flask,render_template,request, session, Blueprint, redirect, url_for, request
import sys,datetime,json
import flask_login
from termcolor import colored




app = Flask(__name__)




loggedIn = False

openIssues = []
closedIssues = []


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






@app.route("/issue-tracker",methods=['GET','POST'])#get well, gets and post sends

def addOrRemoveIssue():
    def updatePage():
        print("RAN UPDATE")
        
        return render_template("issue-tracker.html",issueList=openIssues,closeIssueList=closedIssues)

    def addIssue():
        print("test2")
        issueName = request.form.get("issueName")
        issueDescription = request.form.get("issueDescription")
        assignee = request.form.get("assignee")
        creator = request.form.get("creator")
        severityButton = request.form.get("exampleRadios")

        #print(issueName,issueDescription,assignee)

        openIssueFiles = open("openIssues.txt","a+")


        if issueName == "" or issueDescription == "" or assignee == "":
            
            return render_template("issue-tracker.html",errorMessage = "Error: Not all values submitted!")
        date_object = datetime.date.today()
        try:
            issueFormat = "Issue Severity Level: " + severityButton + "\n" + "Name: "+ issueName + "\n" + "Description:" + issueDescription +"\n"+ "Assigned To: " + assignee + "\n"+ "Date Created: " +str(date_object) + "\n\n" + "This issue was logged by: " + creator
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