import os


def readGraph(file_graph):

    TheGraph = open(file_graph, 'r')
    all_arcs = TheGraph.readlines()
    TheGraph.close()

    return all_arcs


def getOrigDest(all_arcs):

    Origine = []
    Destination = []
    for one_arc in all_arcs:
        this_arc = one_arc.split("\t")
        orig = int(this_arc[0])
        dest = int(this_arc[1].strip("\n"))
        Origine.append(orig)
        Destination.append(dest)

    return {'orig': Origine, 'dest': Destination}


def getNbArcVert(Origine, Destination):
    return {'NbArcs': len(Origine), 'NbVertices': max(max(Origine), max(Destination))+1}


# numsucc: numero de l'arc succ
# numprec: numero de l'arc prec
def getSuccPrec(Origine, Destination):

    infoNbArcVert = getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    # la liste des successeurs de i
    # succ = new [len(NbVertices2)][] en java
    succ = [[] for i in range(NbVertices)]
    # Numero de l'arc successeur de i
    numsucc = [[] for i in range(NbVertices)]
    # Numero des arcs prÃ©cedents
    numprec = [[] for i in range(NbVertices)]
    # la liste des pÃ©dÃ©cesseurs de i
    prec = [[] for i in range(NbVertices)]

    for u in range(0, NbArcs):
        i = Origine[u]
        j = Destination[u]
        succ[i].append(j)
        numsucc[i].append(u)
        prec[j].append(i)
        numprec[j].append(u)

    return {'succ': succ, 'prec': prec, 'numsucc': numsucc, 'numprec': numprec}


# _nsucc: numero de l'arc succ
# _nprec: numero de l'arc prec
def getABSuccPrec(Origine, Destination):

    infoNbArcVert = getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    infoSuccPrec = getSuccPrec(Origine, Destination)
    succ = infoSuccPrec['succ']
    numsucc = infoSuccPrec['numsucc']
    prec = infoSuccPrec['prec']
    numprec = infoSuccPrec['numprec']

    _asucc = []
    _bsucc = []
    _nsucc = []
    _inds = 0

    for j in range(0, NbVertices):
        _asucc.append(_inds)
        _inds = _inds + len(succ[j])
        _bsucc = _bsucc + succ[j]
        _nsucc = _nsucc + numsucc[j]

    _asucc.append(_inds)

    _aprec = []
    _bprec = []
    _nprec = []
    _inds = 0

    for j in range(0, NbVertices):
        _aprec.append(_inds)
        _inds = _inds + len(prec[j])
        _bprec = _bprec + prec[j]
        _nprec = _nprec + numprec[j]
    _aprec.append(_inds)

    return {'_asucc': _asucc, '_bsucc': _bsucc, '_nsucc': _nsucc, '_aprec': _aprec, '_bprec': _bprec, '_nprec': _nprec}
