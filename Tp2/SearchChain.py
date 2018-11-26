import ReadGraph


def SearchChain(Origine, Destination, dep, arr):

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    # NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    infoSuccPrec = ReadGraph.getSuccPrec(Origine, Destination)
    succ = infoSuccPrec['succ']
    # numsucc = infoSuccPrec['numsucc']
    prec = infoSuccPrec['prec']
    # numprec = infoSuccPrec['numprec']

    Marked = [False for j in range(0, NbVertices)]
    Predecessor = [-1 for j in range(0, NbVertices)]
    Successor = [-1 for j in range(0, NbVertices)]

    In_Stack = [False for j in range(0, NbVertices)]
    List = []
    List.append(dep)
    Found = False

    while(List != [] and not Found):
        j = List[0]
        del(List[0])
        Marked[j] = True

        for k in succ[j]:
            if (k == arr):
                Found = True
            if(not In_Stack[k]):
                List.append(k)
                In_Stack[k] = True
                Predecessor[k] = j
        for k in prec[j]:
            if (k == arr):
                Found = True
            if(not In_Stack[k]):
                List.append(k)
                In_Stack[k] = True
                Successor[k] = j

    return {'result': Found, 'Predecessor': Predecessor, 'Successor': Successor}


def SearchChain_ts(Origine, Destination, u0):

    dep = Origine[u0]
    arr = Destination[u0]

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    # NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    infoABSuccPrec = ReadGraph.getABSuccPrec(Origine, Destination)

    _aprec = infoABSuccPrec['_aprec']
    _bprec = infoABSuccPrec['_bprec']
    _nprec = infoABSuccPrec['_nprec']

    _asucc = infoABSuccPrec['_asucc']
    _bsucc = infoABSuccPrec['_bsucc']
    _nsucc = infoABSuccPrec['_nsucc']

    Marked = [False for j in range(0, NbVertices)]
    Predecessor = [-1 for j in range(0, NbVertices)]
    Successor = [-1 for j in range(0, NbVertices)]

    In_Stack = [False for j in range(0, NbVertices)]
    List = []
    List.append(dep)
    Found = False

    while(List != [] and not Found):
        i = List[0]
        del(List[0])
        Marked[i] = True

        for j in range(_asucc[i], _asucc[i+1]):
            the_succ = _bsucc[j]
            the_arc = _nsucc[j]

            if the_arc == u0:
                continue

            if (the_succ == arr):
                Found = True
            if(not In_Stack[the_succ]):
                List.append(the_succ)
                In_Stack[the_succ] = True
                Predecessor[the_succ] = i

        for j in range(_aprec[i], _aprec[i+1]):
            the_prec = _bprec[j]
            the_arc = _nprec[j]

            if (the_prec == arr):
                Found = True
            if(not In_Stack[the_prec]):
                List.append(the_prec)
                In_Stack[the_prec] = True
                Successor[the_prec] = i

    return {'result': Found, 'Predecessor': Predecessor, 'Successor': Successor}


def IdentifyChain(Origine, Destination, dep, arr):

    resultSearchChain = SearchChain(Origine, Destination, dep, arr)

    if resultSearchChain['result']:
        Predecessor = resultSearchChain['Predecessor']
        Successor = resultSearchChain['Successor']

        The_chain = []
        mu_plus = []
        mu_minus = []

        infoABSuccPrec = ReadGraph.getABSuccPrec(Origine, Destination)

        _aprec = infoABSuccPrec['_aprec']
        _bprec = infoABSuccPrec['_bprec']
        _nprec = infoABSuccPrec['_nprec']

        _asucc = infoABSuccPrec['_asucc']
        _bsucc = infoABSuccPrec['_bsucc']
        _nsucc = infoABSuccPrec['_nsucc']

        i = arr
        while i != dep:
            # arc(k, i)
            k = Predecessor[i]

            # search the number of the arc (k,i) and add this arc to the list The_chain
            # depending on the color of u0, add this arc to mu_plus or to mu_minus
            for j in range(_asucc[k], _asucc[k+1]):
                the_succ = _bsucc[j]
                the_arc = _nsucc[j]
                if the_succ == i:
                    The_chain.append(the_arc)
                    mu_plus.append(the_arc)

            i = Predecessor[i]

        while i != dep:
            # arc(k, i)
            k = Successor[i]

            # search the number of the arc (k,i) and add this arc to the list The_chain
            # depending on the color of u0, add this arc to mu_plus or to mu_minus
            for j in range(_aprec[k], _aprec[k+1]):
                the_prec = _bprec[j]
                the_arc = _nprec[j]
                if the_prec == i:
                    The_chain.append(the_arc)
                    mu_minus.append(the_arc)

            i = Successor[i]

        print(Predecessor)
        print(Successor)
        print(The_chain)
        print(mu_plus)
        print(mu_minus)

        return True

    else:
        return False


def IdentifyChain_ts(Origine, Destination, u0):

    resultSearchChain = SearchChain_ts(Origine, Destination, u0)

    if resultSearchChain['result']:
        Predecessor = resultSearchChain['Predecessor']
        Successor = resultSearchChain['Successor']

        The_chain = []
        mu_plus = []
        mu_minus = []

        infoABSuccPrec = ReadGraph.getABSuccPrec(Origine, Destination)

        _aprec = infoABSuccPrec['_aprec']
        _bprec = infoABSuccPrec['_bprec']
        _nprec = infoABSuccPrec['_nprec']

        _asucc = infoABSuccPrec['_asucc']
        _bsucc = infoABSuccPrec['_bsucc']
        _nsucc = infoABSuccPrec['_nsucc']

        dep = Origine[u0]
        arr = Destination[u0]

        i = arr
        while i != dep:
            if Predecessor[i] == -1:
                break

            # arc(k, i)
            k = Predecessor[i]

            # search the number of the arc (k,i) and add this arc to the list The_chain
            # depending on the color of u0, add this arc to mu_plus or to mu_minus
            for j in range(_asucc[k], _asucc[k+1]):
                the_succ = _bsucc[j]
                the_arc = _nsucc[j]
                if the_succ == i:
                    The_chain.append(the_arc)
                    mu_plus.append(the_arc)

            i = Predecessor[i]

        while i != dep:
            if Successor[i] == -1:
                break
            # arc(k, i)
            k = Successor[i]

            # search the number of the arc (k,i) and add this arc to the list The_chain
            # depending on the color of u0, add this arc to mu_plus or to mu_minus
            for j in range(_aprec[k], _aprec[k+1]):
                the_prec = _bprec[j]
                the_arc = _nprec[j]
                if the_prec == i:
                    The_chain.append(the_arc)
                    mu_minus.append(the_arc)

            i = Successor[i]

        return {'The_chain': The_chain, 'mu_plus': mu_plus, 'mu_minus': mu_minus}

    else:
        return False
