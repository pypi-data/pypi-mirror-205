from pyccel.decorators import types
from numpy import shape
@types("float64[:,:,:,:,:,:]", "float64[:,:,:]", "float64[:,:,:]")
def lo_dot_9vfx58u7(mat00, x0, out0):

    
    for i1 in range(0, 2, 1):
        for i2 in range(0, 2, 1):
            for i3 in range(0, 64, 1):
                v00 = 0.0
                for k1 in range(0, 3, 1):
                    for k2 in range(0, 3, 1):
                        for k3 in range(0, 7, 1):
                            v00 += mat00[1 + i1,1 + i2,3 + i3,k1,k2,k3]*x0[i1 + k1,i2 + k2,i3 + k3]
                        
                    
                
                out0[1 + i1,1 + i2,3 + i3] = v00
            
        
    
    return