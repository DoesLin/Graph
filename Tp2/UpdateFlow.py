import ReadGraph


def UpdateColor(infoOrigDestCpty, Flow, Color, Color_succ, Color_prec, u):

    Origine = infoOrigDestCpty['orig']
    Destination = infoOrigDestCpty['dest']
    MaxCapacity = infoOrigDestCpty['maxCpty']
    MinCapacity = infoOrigDestCpty['minCpty']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    infoSuccPrec = ReadGraph.getSuccPrec(Origine, Destination)
    succ = infoSuccPrec['succ']
    # numsucc = infoSuccPrec['numsucc']
    prec = infoSuccPrec['prec']
    # numprec = infoSuccPrec['numprec']

    for u in range(0, NbArcs):
        i = Origine[u]
        j = Destination[u]
        if Flow[u] > MinCapacity[u] and Flow[u] < MaxCapacity[u]:
            Color[u] = 'R'
        if Flow[u] <= MinCapacity[u]:
            Color[u] = 'N'
        if Flow[u] >= MaxCapacity[u]:
            Color[u] = 'V'
        Color_succ[i][succ[i].index(j)] = Color[u]
        Color_prec[j][prec[j].index(i)] = Color[u]
