from pyccel.decorators import types
from numpy import shape
@types("float64[:,:]", "float64[:]", "float64[:]")
def lo_dot_db6rmr7n(mat, x, out):

    
    for i1 in range(0, 4, 1):
        v = 0.0
        for k1 in range(0, 3, 1):
            v += mat[2 + i1,k1]*x[1 + i1 + k1]
        
        out[2 + i1] = v
    
    return