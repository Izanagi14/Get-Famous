import numpy as np
a = np.ones(5)
a1 = 0
b = np.zeros((4,10))
#c = np.c_[a,b]
d = np.array(a[:]) >= a1
e = b[:,:-1]
print(e)
#print(d)
#print(c)