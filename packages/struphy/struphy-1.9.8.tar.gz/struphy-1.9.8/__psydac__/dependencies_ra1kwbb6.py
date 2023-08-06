from pyccel.decorators import types
from numpy import shape
@types("float64[:,:,:,:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "int64", "int64", "int64", "int64", "int64", "int64")
def lo_dot_ra1kwbb6(mat, x, out, s1, s2, s3, n1, n2, n3):

    
    for i1 in range(0, n1, 1):
        for i2 in range(0, n2, 1):
            for i3 in range(0, n3, 1):
                v = 0.0
                for k1 in range(0, 5, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v += mat[2 + i1,2 + i2,3 + i3,k1,k2,k3]*x[i1 + k1,i2 + k2,i3 + k3]
                        
                    
                
                out[2 + i1,2 + i2,3 + i3] = v
            
        
    
    return