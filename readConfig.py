import json

class ReadConfig:

    def __init__(self,filename):
        self.filename=filename
        self.__checkIfFileExists()

        self.file= open(self.filename, "r")
        self.datiJson = json.load(self.file)

        self.clients=self.getClients()


    def __checkIfFileExists(self):
        try:
            f = open(self.filename,'r')
        except:
            raise FileNotFoundError("Can't open file "+self.filename)

    def getFilename(self) -> str:
        return self.filename


    def getClients(self) -> list:
        return self.datiJson["clienti"]

    def getNumeroClienti(self) -> int:
        return self.clients.__len__()

    def getAttributoCliente(self, scelta, attributo) -> str:
        return self.clients[scelta-1][attributo]

    def getNomeCliente(self,scelta) -> str:
        return self.getAttributoCliente(scelta, "nome")

    def getIndirizzoCliente(self,scelta) -> str:
        return self.getAttributoCliente(scelta, "indirizzo")


    def getVm(self) -> str:
        return self.datiJson["vm_name"]


    def getFileFix(self) -> str:
        return self.datiJson["file_fix"]


    def getOptions(self) -> str:
        return self.datiJson["opzioni"]




   
