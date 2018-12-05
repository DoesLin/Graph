import ReadGraph


def InitColor(Origine, Destination):

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    Color = ['-' for j in range(0, NbArcs)]
    Color_succ = [[] for i in range(NbVertices)]
    Color_prec = [[] for i in range(NbVertices)]
    Flow = [0] * NbArcs

    for u in range(0, NbArcs):
        Color_succ[Origine[u]].append('N')
        Color_prec[Destination[u]].append('N')

    Predecessor = [-1 for j in range(0, NbVertices)]
    Successor = [-1 for j in range(0, NbVertices)]
    Marked = [0 for j in range(0, NbVertices)]
    Chain = []

    return {'Flow': Flow, 'Color': Color, 'Color_succ': Color_succ, 'Color_prec': Color_prec, 'Chain': Chain,
            'Predecessor': Predecessor, 'Successor': Successor, 'Marked': Marked}


def UpdateColor(infoOrigDestCpty, infoSuccPrec, infoColor, u):

    Origine = infoOrigDestCpty['orig']
    Destination = infoOrigDestCpty['dest']
    MaxCapacity = infoOrigDestCpty['maxCpty']
    MinCapacity = infoOrigDestCpty['minCpty']

    succ = infoSuccPrec['succ']
    prec = infoSuccPrec['prec']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    for u in range(0, NbArcs):
        i = Origine[u]
        j = Destination[u]
        if infoColor['Flow'][u] > MinCapacity[u] and infoColor['Flow'][u] < MaxCapacity[u]:
            infoColor['Color'][u] = 'R'
        if infoColor['Flow'][u] <= MinCapacity[u]:
            infoColor['Color'][u] = 'N'
        if infoColor['Flow'][u] >= MaxCapacity[u]:
            infoColor['Color'][u] = 'V'
        infoColor['Color_succ'][i][succ[i].index(j)] = infoColor['Color'][u]
        infoColor['Color_prec'][j][prec[j].index(i)] = infoColor['Color'][u]

    return infoColor


def UpdateFlow(infoOrigDestCpty, infoSuccPrec, infoColor):

    # print('Flow', infoColor['Flow'])
    # print('Chain', infoColor['Chain'])
    MaxCapacity = infoOrigDestCpty['maxCpty']
    MinCapacity = infoOrigDestCpty['minCpty']
    episilon = 999999
    for i in infoColor['Chain']:
        u = i[0]
        sens = i[1]
        if sens == 1:
            episilon = min(episilon, MaxCapacity[u] - infoColor['Flow'][u])
        else:
            episilon = min(episilon, infoColor['Flow'][u] - MinCapacity[u])
    for i in infoColor['Chain']:
        u = i[0]
        sens = i[1]
        infoColor['Flow'][u] += episilon * sens

    return infoColor
