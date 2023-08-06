from pyccel.decorators import types
@types("float64[:,:,:,:]", "float64[:,:,:,:]", "int64[:]", "float64[:,:]", "int64", "int64", "int64", "int64", "int64", "float64[:,:]", "int64", "int64")
def assemble_matrix_reyksvpz(global_test_basis_v_1, global_trial_basis_u_1, global_span_v_1, global_x1, test_v_p1, trial_u_p1, n_element_1, k1, pad1, g_mat_u_v_reyksvpz, b01, e01):

    from numpy import array, zeros, zeros_like, floor
    local_x1 = zeros_like(global_x1[0,:])
    
    l_mat_u_v_reyksvpz = zeros((2, 3), dtype='float64')
    for i_element_1 in range(0, n_element_1, 1):
        local_x1[:] = global_x1[i_element_1,:]
        span_v_1 = global_span_v_1[i_element_1]
        for i_basis_1 in range(0, 2, 1):
            for j_basis_1 in range(0, 2, 1):
                contribution_v_u_reyksvpz = 0.0
                for i_quad_1 in range(0, 3, 1):
                    x1 = local_x1[i_quad_1]
                    v_1 = global_test_basis_v_1[i_element_1,i_basis_1,0,i_quad_1]
                    v_1_x1 = global_test_basis_v_1[i_element_1,i_basis_1,1,i_quad_1]
                    u_1 = global_trial_basis_u_1[i_element_1,j_basis_1,0,i_quad_1]
                    u_1_x1 = global_trial_basis_u_1[i_element_1,j_basis_1,1,i_quad_1]
                    v = v_1
                    v_x1 = v_1_x1
                    u = u_1
                    u_x1 = u_1_x1
                    contribution_v_u_reyksvpz += u*v
                
                l_mat_u_v_reyksvpz[i_basis_1,1 - i_basis_1 + j_basis_1] = contribution_v_u_reyksvpz
            
        
        g_mat_u_v_reyksvpz[pad1 + span_v_1 - test_v_p1:1 + pad1 + span_v_1,:] += l_mat_u_v_reyksvpz[:,:]
    
    return