import math, vector

p4=(1,2,3,4)

class particle:
    def __init__(self,px,py,pz,m):#{inizia qua perché dopo ha un'indentazione diversa
        self.px = px
        self.py = py
        self.pz = pz
        self.m = m
        self.e = math.sqrt(m**2+(px**2+py**2+pz**2))
        #p4=3
        #rimanente=3.1
        self.p4=(self.px,self.py,self.pz,self.e)
    #}per segnalare che la funzione è finita non uso un carattere ma un'indentazione diversa
    def particle_p4(self,lorentz_p4):
        return particle(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, m=lorentz_p4.m)

    def init_p4(self,lorentz_p4,charge):
        self.__init__(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, m=lorentz_p4.m)
