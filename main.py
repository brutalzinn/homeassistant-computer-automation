from ipaddress import ip_address
from telnetlib import IP
from flask import Flask
from flask_restful import Resource, Api
import imaplib
from email.header import decode_header
import webbrowser
import psutil
import os
import conversions
from conversions import bytes2human
from dotenv import load_dotenv
load_dotenv()
# use your email id here
username = os.getenv("EMAIL")
password =  os.getenv("SECRET")


app = Flask(__name__)
api = Api(app)
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

class HelloHomeAssistant(Resource):
    def post(self):
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        result = imap.login(username, password) 
        imap.select() 
        response, messages = imap.search(None, 'UnSeen')
        messages = messages[0].split()
  
        latest = int(messages[-1])
        emails = int(latest) - int(latest-20)
        print("conectado com sucesso.")
        return {"status":True, "email":emails}
        
class HelloPaladins(Resource):
    def post(self):
        if(checkIfProcessRunning("paladins")):
            return {"status":False,"message":"Não foi possível abrir paladins. Paladins já está em execução."}
        os.startfile("steam://rungameid/444090")
        return {"status":True,"message":"Paladins iniciado com sucesso, Roberto!"}

class HelloRoblox(Resource):
    def post(self):
        webbrowser.open("https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator", new=2)
        return {"status":True,"message":"Bee Swarm Simulator iniciado com sucesso, Roberto!"}

class ComputerInfo(Resource):
    def post(self):
        mem_usage = psutil.virtual_memory()
        total_mem = bytes2human(mem_usage[0],symbols='customary_ext')
        used_mem = bytes2human(mem_usage[3],symbols='customary_ext')
        resultado =  f"{used_mem} de {total_mem} RAM usada."
        return {"status":True,"message":resultado}

api.add_resource(HelloHomeAssistant, '/email')
api.add_resource(HelloPaladins, '/paladins')
api.add_resource(HelloRoblox, '/roblox')
api.add_resource(ComputerInfo, '/computer')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=3030)