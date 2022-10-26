import math

class particle:
    def __init__(self,px,py,pz,m):
        self._px = px
        self._py = py
        self._pz = pz
        self._m = m
        self._e = math.sqrt(m**2+(px**2+py**2+pz**2))
        self._p4=(self._px,self._py,self._pz,self._e)

        
class charged_particle(particle):
    def __init__(self,px,py,pz,m=-1,e=-1,charge=None):
        super().__init__(px,py,pz,m)
        self._charge=charge
        if(m!=-1):
            self._m = m
            self._e = math.sqrt(m**2+(px**2+py**2+pz**2))
        if(e!=-1):
            self._e = e
            self._m = math.sqrt(e**2-(px**2+py**2+pz**2))
        self._p4=(self._px,self._py,self._pz,self._e)
      
    @property
    def px(self):
        return self._px
    @px.setter
    def px(self,px):
        self._px = px


    @property
    def py(self):
        return self._py
    @property
    def pz(self):
        return self._pz
    @property
    def e(self):
        return self._e
    @property
    def m(self):
        return self._m
    @property
    def p4(self):
        return self._p4

    @py.setter
    def py(self):
        return self._px
    @pz.setter
    def pz(self):
        return self._px
    @e.setter
    def e(self):
        return self._px
    @m.setter
    def m(self):
        return self._px

    
    
    

        
