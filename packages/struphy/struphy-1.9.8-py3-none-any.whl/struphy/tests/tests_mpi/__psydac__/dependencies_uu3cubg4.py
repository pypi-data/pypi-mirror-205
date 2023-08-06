from pyccel.decorators import types
from numpy import shape
@types("float64[:,:,:,:,:,:]", "float64[:,:,:,:,:,:]", "float64[:,:,:,:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "float64[:,:,:]", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64", "int64")
def lo_dot_uu3cubg4(mat00, mat11, mat22, x0, x1, x2, out0, out1, out2, s00_1, s00_2, s00_3, s11_1, s11_2, s11_3, s22_1, s22_2, s22_3, n00_1, n00_2, n00_3, n11_1, n11_2, n11_3, n22_1, n22_2, n22_3, ne00_1, ne00_2, ne00_3, ne11_1, ne11_2, ne11_3, ne22_1, ne22_2, ne22_3):

    
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
            
        
    
    for i1 in range(0, n11_1, 1):
        for i2 in range(0, n11_2, 1):
            for i3 in range(0, n11_3, 1):
                v11 = 0.0
                for k1 in range(0, 5, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v11 += mat11[2 + i1,2 + i2,3 + i3,k1,k2,k3]*x1[i1 + k1,i2 + k2,i3 + k3]
                        
                    
                
                out1[2 + i1,2 + i2,3 + i3] = v11
            
        
    
    for i1 in range(0, ne11_1, 1):
        for i2 in range(0, n11_2, 1):
            for i3 in range(0, n11_3, 1):
                v11 = 0.0
                for k1 in range(0, 4 - i1, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v11 += x1[i1 + k1 + n11_1,i2 + k2,i3 + k3]*mat11[2 + i1 + n11_1,2 + i2,3 + i3,k1,k2,k3]
                        
                    
                
                out1[2 + i1 + n11_1,2 + i2,3 + i3] = v11
            
        
    
    for i1 in range(0, n11_1 + ne11_1, 1):
        for i2 in range(0, ne11_2, 1):
            for i3 in range(0, n11_3, 1):
                v11 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n11_1 + 1), 1):
                    for k2 in range(0, 4 - i2, 1):
                        for k3 in range(0, 7, 1):
                            v11 += x1[i1 + k1,i2 + k2 + n11_2,i3 + k3]*mat11[2 + i1,2 + i2 + n11_2,3 + i3,k1,k2,k3]
                        
                    
                
                out1[2 + i1,2 + i2 + n11_2,3 + i3] = v11
            
        
    
    for i1 in range(0, n11_1 + ne11_1, 1):
        for i2 in range(0, n11_2 + ne11_2, 1):
            for i3 in range(0, ne11_3, 1):
                v11 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n11_1 + 1), 1):
                    for k2 in range(0, 5 - max(0, i2 - n11_2 + 1), 1):
                        for k3 in range(0, 6 - i3, 1):
                            v11 += x1[i1 + k1,i2 + k2,i3 + k3 + n11_3]*mat11[2 + i1,2 + i2,3 + i3 + n11_3,k1,k2,k3]
                        
                    
                
                out1[2 + i1,2 + i2,3 + i3 + n11_3] = v11
            
        
    
    for i1 in range(0, n22_1, 1):
        for i2 in range(0, n22_2, 1):
            for i3 in range(0, n22_3, 1):
                v22 = 0.0
                for k1 in range(0, 5, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v22 += mat22[2 + i1,2 + i2,3 + i3,k1,k2,k3]*x2[i1 + k1,i2 + k2,i3 + k3]
                        
                    
                
                out2[2 + i1,2 + i2,3 + i3] = v22
            
        
    
    for i1 in range(0, ne22_1, 1):
        for i2 in range(0, n22_2, 1):
            for i3 in range(0, n22_3, 1):
                v22 = 0.0
                for k1 in range(0, 4 - i1, 1):
                    for k2 in range(0, 5, 1):
                        for k3 in range(0, 7, 1):
                            v22 += x2[i1 + k1 + n22_1,i2 + k2,i3 + k3]*mat22[2 + i1 + n22_1,2 + i2,3 + i3,k1,k2,k3]
                        
                    
                
                out2[2 + i1 + n22_1,2 + i2,3 + i3] = v22
            
        
    
    for i1 in range(0, n22_1 + ne22_1, 1):
        for i2 in range(0, ne22_2, 1):
            for i3 in range(0, n22_3, 1):
                v22 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n22_1 + 1), 1):
                    for k2 in range(0, 4 - i2, 1):
                        for k3 in range(0, 7, 1):
                            v22 += x2[i1 + k1,i2 + k2 + n22_2,i3 + k3]*mat22[2 + i1,2 + i2 + n22_2,3 + i3,k1,k2,k3]
                        
                    
                
                out2[2 + i1,2 + i2 + n22_2,3 + i3] = v22
            
        
    
    for i1 in range(0, n22_1 + ne22_1, 1):
        for i2 in range(0, n22_2 + ne22_2, 1):
            for i3 in range(0, ne22_3, 1):
                v22 = 0.0
                for k1 in range(0, 5 - max(0, i1 - n22_1 + 1), 1):
                    for k2 in range(0, 5 - max(0, i2 - n22_2 + 1), 1):
                        for k3 in range(0, 6 - i3, 1):
                            v22 += x2[i1 + k1,i2 + k2,i3 + k3 + n22_3]*mat22[2 + i1,2 + i2,3 + i3 + n22_3,k1,k2,k3]
                        
                    
                
                out2[2 + i1,2 + i2,3 + i3 + n22_3] = v22
            
        
    
    return