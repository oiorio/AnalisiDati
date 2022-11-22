#!/usr/bin/env python
# coding: utf-8

# In[94]:


import ROOT
import scipy.special
import scipy.stats 
from array import array


# In[78]:


class binomial:
    def __init__(self,p,N):
        self.p=p
        self.N=N

    
    def prob(self,n):
        return scipy.special.comb(self.N,n)*(self.p**n) * (1-self.p)**(self.N-n)

    def low_int(self,o):
        ptot=0
        for n in range(0,o+1):
            ptot=ptot+self.prob(n)
        return ptot
    def up_int(self,o):
        return 1-self.low_int(o-1)

    def upper_limit_p(self, o, alpha=0.05,pscan=100,verbose=0):
        pvec=[pi * 1/pscan for pi in range(0,pscan+1) ]
        a=0
        ul=-1
        p_prec=self.p
        for pi in pvec:
            self.p=pi
            a=self.low_int(o)
            if(verbose>0):print("p scan: ",self.p, " obs: ",o," low integral ",a," alpha ",alpha)
            if (a<alpha):
                ul=pi
                break
        self.p=p_prec
        return ul

    def clopper_pearson(self,o,alpha=0.05,pscan=1000,verbose=0):
        pvec=[pi * 1/pscan for pi in range(0,pscan+1) ]
        a1=10
        a2=10
        uls=[]
        lls=[]
        p_prec=self.p
        for pi in pvec:
            self.p=pi
            a1=self.low_int(o)
            a2=self.up_int(o)
            if(verbose>0):print("p scan: ",self.p, " obs: ",o," low integral ",a1," up integral", a2, " alpha ",alpha)
            if (a1<alpha/2.):
                uls.append(pi)
            if (a2<alpha/2.):
                lls.append(pi)
        ul=1
        ll=0
        if(len(uls)):
            ul=min(uls)
        if(len(lls)):
            ll=max(lls)
        self.p=p_prec

    
        interval=(ll,ul)
        return interval
    def generate(self,ngen=1):
        return scipy.stats.binom.rvs(n=self.N,p=self.p)
    
    def cp_coverage(self,alpha=0.05,n_pseudoexperiments=1000,pscan=1000,verbose=0):
        n_hit=0.0
        for k in range(0,n_pseudoexperiments):
            ki=self.generate()
            interval=self.clopper_pearson(o=ki,alpha=alpha,verbose=verbose-1)
            isInInt=self.p>interval[0] and self.p<interval[1]
            if(verbose>0):print("ki",ki,"interval",interval, " p ", self.p, "is in interval? ",isInInt)
            if (isInInt):
                n_hit=n_hit+1
                
        return n_hit/n_pseudoexperiments


# In[79]:


b=binomial(p=0.5,N=10)


# In[80]:


b.upper_limit_p(o=4,verbose=0,pscan=10000)


# In[81]:


b.clopper_pearson(4,verbose=0,pscan=100000)


# In[85]:


b.cp_coverage(alpha=0.3173,verbose=0,n_pseudoexperiments=1000,pscan=100) 
#a = 0.05 <-->1-a=0.95 <--> 2 sigma 
#a = 0.32 <-->1-a=0.68 <--> 1 sigma 


# In[86]:


b.p=0.5
b.cp_coverage(alpha=0.3173,verbose=0,n_pseudoexperiments=1000,pscan=100) 


# ## Esercizio #1:
# 
# Proviamo a riprodurre il plot della coverage in funzione di p
# 
# ## Esercizion #2:
# 
# Proviamo a valutare il limite di una distribuzione di Poisson
# 
# 

# In[ ]:





# In[ ]:




