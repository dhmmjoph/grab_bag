'''
	MatchUpdater v1.0, (c) 2016 by John Holbrook (VRC 8768A BACKDRIVE)
	Released under the MIT License.

	Third-Party Modules Required:
		pyshorteners: https://github.com/ellisonleao/pyshorteners
'''
import urllib, json, os
from pyshorteners import Shortener

"""CHANGE THESE VARIABLES TO SUIT YOUR TEAM AND TOURNAMENT"""
team = "8768A"
eventSKU = "RE-VRC-16-3693"
"""END OF VARIABLES TO CHANGE FOR DIFFERENT TEAMS OR TOURNAMENTS"""

with open("ifkey.txt", "r") as keyFile:#read-only
	ifKey = keyFile.read()

shortenerAPIKey = open("URLShortenerKey", "r").read()

def isTeamInMatch(match):
	if (match["red1"] == team) or (match["red2"] == team) or (match["red3"] == team):
		return True
	elif (match["blue1"] == team) or (match["blue2"] == team) or (match["blue3"] == team):
		return True
	else:
		return False

def getMatchTitle(match): #returns a string containing the round and number of the match
	title = ""
	thisRound = int(match["round"])
	rounds = ["", "Practice Match ", "Qualification Match ", "Quarter Final ", "Semifinal ", "Final "]
	title += rounds[thisRound]
	if thisRound > 2: #if it's an elimination match
		title += match["instance"]
		title += "-"
	title += match["matchnum"]
	return title

def whichAllianceIsTeamOn(match):
	if team in [match["red1"], match["red2"], match["red3"]]:
		return "red"
	elif team in [match["blue1"], match["blue2"], match["blue3"]]:
		return "blue"

def getWinningAlliance(match):
	redScore = int(match["redscore"])
	blueScore = int(match["bluescore"])
	if redScore > blueScore:
		return "red"
	elif blueScore > redScore:
		return "blue"
	elif blueScore == redScore:
		return "tie"

def didTeamWin(match): #returns 1 for a win, 0 for a tie, or -1 for a loss
	if (whichAllianceIsTeamOn(match) == getWinningAlliance(match)):
		return 1
	elif getWinningAlliance(match) == "tie":
		return 0
	else:
		return -1

def getScore(match): #returns the score as a string, with the winning alliance's score first
	if getWinningAlliance(match) == "red":
		return match["redscore"] + "-" + match["bluescore"]
	elif getWinningAlliance(match) == "blue":
		return match["bluescore"] + "-" + match["redscore"]
	elif getWinningAlliance(match) == "tie":
		return match["bluescore"] + "-" + match["redscore"]

def getTeamAlliance(match): #returns a string of the format "[team] and [team]"
	color = whichAllianceIsTeamOn(match)
	if match[color+"3"] == "": #deals with two-team alliances
		return match[color+"1"] + " and " + match[color+"2"]
	else: #include only the two out of three teams playing in this match
		if match[color+"1"] == match[color+"sit"]:
			alliance = match[color+"2"] + " and " + match[color+"3"]
		elif match[color+"2"] == match[color+"sit"]:
			alliance = match[color+"1"] + " and " + match[color+"3"]
		elif match[color+"3"] == match[color+"sit"]:
			alliance = match[color+"1"] + " and " + match[color+"2"]
		return alliance

def getOpposingAlliance(match):
	if whichAllianceIsTeamOn(match) == "red":
		color = "blue"
	else:
		color = "red"
	if match[color+"3"] == "": #deals with two-team alliances
		return match[color+"1"] + " and " + match[color+"2"]
	else: #include only the two out of three teams playing in this match
		if match[color+"1"] == match[color+"sit"]:
			alliance = match[color+"2"] + " and " + match[color+"3"]
		elif match[color+"2"] == match[color+"sit"]:
			alliance = match[color+"1"] + " and " + match[color+"3"]
		elif match[color+"3"] == match[color+"sit"]:
			alliance = match[color+"1"] + " and " + match[color+"2"]
		return alliance

def generateText(match):
	report = ""
	report += "Update: "
	report += getTeamAlliance(match)
	if (didTeamWin(match) == 1):
		report += (" won " + getMatchTitle(match) + " against ")
	elif (didTeamWin(match) == -1):
		report += (" lost " + getMatchTitle(match) + " to ")
	elif (didTeamWin(match) == 0):
		report += (" tied " + getMatchTitle(match) + " with ")
	report += (getOpposingAlliance(match) + ", " + getScore(match))
	report += ". Full Tournament Results: "
	shortener = Shortener('GoogleShortener', api_key=shortenerAPIKey)
	robotEventsURL = "http://www.robotevents.com/%s.html#tabs-results" % eventSKU
	report += shortener.short(robotEventsURL)
	return report

vexDBURL = "http://api.vexdb.io/get_matches?sku=" + eventSKU
response = urllib.urlopen(vexDBURL)
data = json.loads(response.read())
result = data["result"]

for match in result:
	if isTeamInMatch(match):
		matchid = "M" + match["round"] + match["instance"] + match["matchnum"] + " "
		with open(eventSKU, "r+") as log:
			matchesAlreadyFound = log.read()
			if (matchesAlreadyFound.find(matchid) == -1):
				message = generateText(match)
				print message
				requestData = urllib.urlencode({"value1":message})
				ifURL = "http://maker.ifttt.com/trigger/{vrc_update}/with/key/" + ifKey + "?" + requestData
				terminalCommandToExcecute = "curl -X POST " + ifURL
				os.system(terminalCommandToExcecute)
				with open(eventSKU, "a") as log:
					log.write(matchid)

				