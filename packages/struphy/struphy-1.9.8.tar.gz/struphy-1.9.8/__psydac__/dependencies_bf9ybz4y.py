from pyccel.decorators import types
from numpy import shape
@types("float64[:,:]", "float64[:]", "float64[:]")
def lo_dot_bf9ybz4y(mat00, x0, out0):

    
    for i1 in range(0, 14, 1):
        v00 = 0.0
        for k1 in range(0, 7, 1):
            v00 += mat00[3 + i1,k1]*x0[i1 + k1]
        
        out0[3 + i1] = v00
    
    for i1 in range(0, 1, 1):
        v00 = 0.0
        for k1 in range(0, 6 - i1, 1):
            v00 += x0[14 + i1 + k1]*mat00[17 + i1,k1]
        
        out0[17 + i1] = v00
    
    return