from pyccel.decorators import types
from numpy import shape
@types("float64[:,:]", "float64[:]", "float64[:]")
def lo_dot_rlvglfus(mat00, x0, out0):

    
    for i1 in range(0, 12, 1):
        v00 = 0.0
        for k1 in range(0, 3, 1):
            v00 += mat00[1 + i1,k1]*x0[i1 + k1]
        
        out0[1 + i1] = v00
    
    for i1 in range(0, 1, 1):
        v00 = 0.0
        for k1 in range(0, 2 - i1, 1):
            v00 += x0[12 + i1 + k1]*mat00[13 + i1,k1]
        
        out0[13 + i1] = v00
    
    return