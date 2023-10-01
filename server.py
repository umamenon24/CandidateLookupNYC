# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

global x
x=0
f = open("data/data.json", "r")
data = json.load(f)
f.close()  

candidates=[data[i]['name'] for i in range(87)]

pi={
    "Democratic": "D",
    "Republican": "R",
    "Conservative": "C",
    "Medical Freedom": "MF",
    "Working Families": "WF"
}


@app.route("/")
@app.route('/home')
def about():
    global x
    x=0

    return render_template('home.html', candidates=candidates)



@app.route("/lookup")
def macro():
    global x
    x+=1
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()  

    valid=[]
    checktype=[]
    pil=[]
    if x!=1:

        dist=int(request.args.get("dist"))
        #print(dist)
        party=request.args.get('party')
        ends=request.args.get('endorsement')
        if ends!="No preference": ends=int(ends)
        issuesSelected=[request.args.get(f"issue{i}") for i in range(1,24) if request.args.get(f"issue{i}")!=None]

        
        #print(dist,party,issuesSelected)
        for cand in data:
            temp=0
            for i in range(len(issuesSelected)):
                if issuesSelected[i] in cand["issues"]: temp+=1
            
            if (int(cand["district"])==dist or dist==0) and (party in cand["party"] or party=="No preference") and temp==len(issuesSelected) and (ends=='No preference' or len(cand['endorsements'])>=ends):
                valid.append(data.index(cand))
                if cand['party'][0] in ['Republican', 'Conservative', 'Medical Freedom']: checktype.append("badge bg-danger")
                elif cand['party'][0] in ['Democratic', 'Working Families']: checktype.append("badge bg-primary")
                pil.append(pi[cand['party'][0]])
        
    if len(valid)==0 and x!=1: valid0=True 
    else: valid0=False

    return render_template('lookup.html', valid=valid, candidates=candidates, data=data, checktype=checktype, pil=pil, valid0=valid0)

@app.route("/candidates/<candidate>")
def micro(candidate):

    global x
    x = 0
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()  
    att=data[int(candidate)]

    temp=""
    for issue in att['issues']:
        if temp!="": temp+=", "+issue
        else: temp+=issue

    temp1=""
    if isinstance(att['party'], list):
        for party in att['party']:
            if temp1!="": temp1+=", "+party
            else: temp1+=party
    else:
        temp1=att['party']

    partycolor=""

    att1=[f"District: {att['district']}", f"Party affiliation: {temp1}", f"Core platform: {temp}"]
    if 'Republican' in att['party'] or 'Conservative' in att['party'] or 'Medical Freedom' in att['party']: partycolor="badge bg-danger"
    elif 'Democratic' in att['party'] or 'Working Families' in att['party']: partycolor="badge bg-primary"

    if att['ic']=="I": ic="Incumbent"
    else: ic="Challenger"

    return render_template('candidates.html', candidate=int(candidate),att1=att1, candidates=candidates, data=data, partycolor=partycolor, ic=ic, disty=att['district'])

app.run(debug=True)
