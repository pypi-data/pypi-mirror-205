

def transpose_1d( M:'float[:,:]', Mt:'float[:,:]', n1:"int64", nc1:"int64", gp1:"int64", p1:"int64",
                  dm1:"int64", cm1:"int64", nd1:"int64", ndT1:"int64", si1:"int64", sk1:"int64", sl1:"int64"):

    #$ omp parallel default(private) shared(Mt,M) firstprivate( n1,nc1,gp1,p1,dm1,cm1,&
    #$ nd1,ndT1,si1,sk1,sl1)

    d1 = gp1-p1

    #$ omp for schedule(static)
    for x1 in range(n1):
        j1 = dm1*gp1 + x1
        for l1 in range(nd1):

            i1 = si1 + cm1*(x1//dm1) + l1 + d1
            k1 = sk1 + x1%dm1-dm1*(l1//cm1)

            if k1<ndT1 and k1>-1 and l1+sl1<nd1 and i1<nc1:
                Mt[j1, l1+sl1] = M[i1, k1]
    #$ omp end parallel
    return
