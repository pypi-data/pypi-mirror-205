from pyccel.decorators import types
from numpy import shape
@types("float64[:,:,:,:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64")
def lo_dot_3qsxfrp5(mat00, x0, out0, s00_1, s00_2, s00_3, n00_1, n00_2, n00_3, ne00_1, ne00_2, ne00_3):

    
    for i1 in range(0, n00_1, 1):
        for i2 in range(0, n00_2, 1):
            for i3 in range(0, n00_3, 1):
                v00 = 0.0
                for k1 in range(0, 5, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v00 += mat00[2 + i1,2 + i2,3 + i3,k1,k2,k3]*x0[i1 + k1,i2 + k2,i3 + k3]
                        
                    
                
                out0[2 + i1,2 + i2,3 + i3] = v00
            
        
    
    for i1 in range(0, ne00_1, 1):
        for i2 in range(0, n00_2, 1):
            for i3 in range(0, n00_3, 1):
                v00 = 0.0
                for k1 in range(0, 4 - i1, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v00 += x0[i1 + k1 + n00_1,i2 + k2,i3 + k3]*mat00[2 + i1 + n00_1,2 + i2,3 + i3,k1,k2,k3]
                        
                    
                
                out0[2 + i1 + n00_1,2 + i2,3 + i3] = v00
            
        
    
    for i1 in range(0, n00_1 + ne00_1, 1):
        for i2 in range(0, ne00_2, 1):
            for i3 in range(0, n00_3, 1):
                v00 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n00_1 + 1), 1):
                    for k2 in range(0, 4 - i2, 1):
                        for k3 in range(0, 7, 1):
                            v00 += x0[i1 + k1,i2 + k2 + n00_2,i3 + k3]*mat00[2 + i1,2 + i2 + n00_2,3 + i3,k1,k2,k3]
                        
                    
                
                out0[2 + i1,2 + i2 + n00_2,3 + i3] = v00
            
        
    
    for i1 in range(0, n00_1 + ne00_1, 1):
        for i2 in range(0, n00_2 + ne00_2, 1):
            for i3 in range(0, ne00_3, 1):
                v00 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n00_1 + 1), 1):
                    for k2 in range(0, 5 - max(0, i2 - n00_2 + 1), 1):
                        for k3 in range(0, 6 - i3, 1):
                            v00 += x0[i1 + k1,i2 + k2,i3 + k3 + n00_3]*mat00[2 + i1,2 + i2,3 + i3 + n00_3,k1,k2,k3]
                        
                    
                
                out0[2 + i1,2 + i2,3 + i3 + n00_3] = v00
            
        
    
    return