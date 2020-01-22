# -*- coding: utf-8 -*-

#---------------------------------------
# Script Import Libraries
#---------------------------------------
import clr
import codecs
import json
import os
import re
import sys

clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Scraper.dll"))
from ScraperTool import Scraper
from System.Collections.Generic import List

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Webster's Dictionary Parameter"
Website = "http://www.twitch.tv/EncryptedThoughts"
Description = "Adds a $dictionary parameter that gets the Webster defintion of a word."
Creator = "EncryptedThoughts"
Version = "1.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
ReadMe = os.path.join(os.path.dirname(__file__), "README.md")

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.EnableDebug = False
            self.EnableLengthLimit = True
            self.LengthLimit = 400

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, SettingsFile):
        try:
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

#---------------------------------------
# Settings functions
#---------------------------------------

def ReloadSettings(jsondata):
    ScriptSettings.Reload(jsondata)

def SaveSettings(self, SettingsFile):
    with codecs.open(SettingsFile, encoding='utf-8-sig', mode='w+') as f:
        json.dump(self.__dict__, f, encoding='utf-8-sig')
    with codecs.open(SettingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
        f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
    return

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):

    regex = "\$dictionary\(\s*\p{L}+\s*\)" # !dictionary(string of any letters from any language)

    item = re.search(regex, parseString)

    if item is None:
        return parseString

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Dictionary request detected, guess we're about to learn once I parse this:  " + item.group())

    word = item.group().strip()[12:][:-1]

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Ripping apart webster page to find this word: " + word)

    paths = List[str](["//div[@id='definition-wrapper'][1]//div[@class='row entry-attr'][1]/div", "//div[@id='definition-wrapper'][1]//div[@id='dictionary-entry-1'][1]/div[@class='vg']"])
    results = json.loads(Scraper.Parse("https://www.merriam-webster.com/dictionary/" + word, paths))

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Results: " + str(results))

    response = ""
    if len(results) < 2:
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, "Not all data returned :(")
        return parseString      
    elif results[0] is None or results[1] is None:
        response = "No definition found for " + word
    else:
        response += ReadDefinition(results[0]) + " | " + ReadDefinition(results[1])

    response = " ".join(response.split())

    if ScriptSettings.EnableLengthLimit:
        response = response[:ScriptSettings.LengthLimit]
    parseString = parseString.replace(item.group(), response)

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Response: " + response)

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Definition obtained. I'm going back to sleep. I've learned enough today...")

    return parseString

def ReadDefinition(node):
    response = ""

    if len(node["attributes"]) > 0 and "class" in node["attributes"][0] and node["attributes"][0]["class"].find("ex-sent") != -1:
        return response

    if "innerText" in node:
        response += node["innerText"]
    else:
        for child in node["children"]:
            response += ReadDefinition(child)

    return response

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def openreadme():
    os.startfile(ReadMe)