import re

class Client:

    def __init__(self, name, address):
        self.checkCorrectValues(name, address)
        self.name=name
        self.address=address
        self.setSubnet(address)


    def checkCorrectValues(self, name, address) -> None:
        if(not isinstance(name,str)): raise ValueError("Name not a String")
        if(not isinstance(address,str) or 
           not re.fullmatch("[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}",address)): raise ValueError("Address not valid")


    def returnValues(self) -> list:
        return [self.name, self.address, self.subnet]


    def getSubnet(self) -> str:
        return self.subnet

    def setSubnet(self,address) -> None:
        self.subnet=address[0:address.rfind(".")]+".0/24"
        if(not re.fullmatch("[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.0\/24",self.subnet)): 
            raise ValueError("Error parsing subnet.")

    def getName(self) -> str:
        return self.name
    
    def setName(self,name) -> None:
        self.name=name

    def getAddress(self) -> str:
        return self.address
    
    def setAddress(self,address) -> None:
        self.address=address

    def toString(self) -> str:
        return "\n[Client]\n  Name:    "+self.getName()+"\n  Address: "+self.getAddress()+"\n  Subnet:  "+self.getSubnet()+"\n"