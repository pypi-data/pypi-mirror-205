from pyccel.decorators import types
from numpy import shape
@types("float64[:,:]", "float64[:]", "float64[:]")
def lo_dot_smhc1gf8(mat00, x0, out0):

    
    for i1 in range(0, 4, 1):
        v00 = 0.0
        for k1 in range(0, 5, 1):
            v00 += mat00[2 + i1,k1]*x0[i1 + k1]
        
        out0[2 + i1] = v00
    
    return