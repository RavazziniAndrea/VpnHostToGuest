import sys
import textwrap
import os
import subprocess
import json
from colorama import Fore, Style

from readConfig import ReadConfig
from client import Client

fileFix = None
config = None
opzioni = None
vm = None


def checkNumeroParams(numParams):
    _check = (numParams == 2 or numParams == 3)
    if not _check: #perchè 0 = nome comando
        print("[ERRORE] Numero parametri errato")
    return _check


def checkParamEsiste(param):
    _checkParam = param in config.getOptions()
    if not _checkParam:
        print("[ERRORE] Parametro non valido")
    
    return _checkParam


def checkNumeroInRange(numero):
    try:
        return (int(numero) > 0 and int(numero) <= config.getNumeroClienti())
    except:
        return False


def getNumeroDaInput():
    return input("Scelta: ")


def scriviListaClienti():
    print("Seleziona cliente:")
    i = 1
    for dato in config.getClients():
        print("  [{}] ".format(i)+dato["nome"])
        i=i+1


def getScelta():
    _length = sys.argv.__len__()
    if not checkNumeroParams(_length) : return -1
    
    param = getParam()
    if not checkParamEsiste(param) : return -2
    numero = 0
    if(_length == 2):
        scriviListaClienti()
        numero = getNumeroDaInput()
    else:
        numero = sys.argv[2]

    while not checkNumeroInRange(numero):
        print("[ERRORE] Numero cliente non valido, reinserire..")
        numero = getNumeroDaInput()

    return numero


def getParam():
    if sys.argv.__len__() < 2:
        print("Numero parametro errato")
        quit()
    return sys.argv[1]


def isVmAccesa():
    return int(subprocess.check_output("vboxmanage list runningvms | grep \""+config.getVm()+"\" | wc -l ", shell=True)) == 1
        

def accendiVmSeSpenta(param):
    if not isVmAccesa(): 
        print("Starting vpn...")
        os.system("vboxmanage startvm "+config.getVm())
        if param != "-s":
            input("Accendere la vpn e premere Invio...")
    else:
        print("VPN vm is already on")


def aggiungiRoute(subnet):
    os.system("sudo ip route add "+subnet+" via 10.0.3.2")
    print("Aggiunta route: "+str(subnet))


def checkPing(ip):
    print("Controllo connessione...")
    pingRes = os.system("ping -c 1 "+ip+" > /dev/null ")
    if pingRes == 0:
        print(Fore.GREEN+"\nConnessione OK!")
    else:
        print(Fore.RED+"\n!!! NON RAGGIUNGIBILE !!!")
    print(Style.RESET_ALL)


def pingContinuo(ip):
    os.system("ping -c 100 "+ip)


def apriFileFixSeRichiesto():
    risposta = input("Devi installare delle fix? [Y/n]")
    if risposta != 'n' and risposta != 'N':
        print("Apertura file...")
        os.system("xdg-open "+config.getFileFix())
        

def rimuoviRoute(subnet):
    os.system("sudo ip route del "+subnet)
    print("Route eliminata")


def showHelp():
    print(textwrap.dedent("""  
    Uso:
    -a	Aggiunge route 
    -d 	Rimuove route
    -p 	Controlla connessione	
    -P 	Ping continuo
    -s  Accende la VM
    -h 	help"""))


def start():
    global config
    config = ReadConfig("config.json")

    param = getParam()

    if param == "-s" or param == "-h":
        if param == "-s":
            accendiVmSeSpenta(param)
        if param == "-h":
            showHelp()
    else:
        scelta = int(getScelta())

        nome = config.getNomeCliente(scelta)
        indirizzo = config.getIndirizzoCliente(scelta)

        if nome == None or indirizzo == None:
            print("[ERRORE] Impossibile leggere nome o indirizzo. Abort()")
            quit()

        client = Client(nome, indirizzo)

        print(client.toString())

        if param == "-a":
            accendiVmSeSpenta(param)
            aggiungiRoute(client.getSubnet())
            checkPing(client.getAddress())
            apriFileFixSeRichiesto()
        elif param == "-p":
            checkPing(client.getAddress())
        elif param == "-P":
            pingContinuo(client.getAddress())
        elif param == "-d":
            rimuoviRoute(client.getSubnet())


if __name__ == "__main__" :
    start()
