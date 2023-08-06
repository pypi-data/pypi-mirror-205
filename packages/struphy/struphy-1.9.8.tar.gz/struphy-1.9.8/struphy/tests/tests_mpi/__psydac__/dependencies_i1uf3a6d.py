from pyccel.decorators import types
from numpy import shape
@types("float64[:,:]", "float64[:]", "float64[:]")
def lo_dot_i1uf3a6d(mat00, x0, out0):

    
    for i1 in range(0, 8, 1):
        v00 = 0.0
        for k1 in range(0, 7, 1):
            v00 += mat00[3 + i1,k1]*x0[i1 + k1]
        
        out0[3 + i1] = v00
    
    return