import ReadGraph


def InitColor(Origine, Destination):

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    Color = ['-' for j in range(0, NbArcs)]
    Color_succ = [[] for i in range(NbVertices)]
    Color_prec = [[] for i in range(NbVertices)]
    Flow = [0] * NbArcs
    Flow = [9, 0, 9, 9, 9]
    Phi = [0] * NbArcs

    for u in range(0, NbArcs):
        Color_succ[Origine[u]].append('N')
        Color_prec[Destination[u]].append('N')

    Predecessor = [-1 for j in range(0, NbVertices)]
    Successor = [-1 for j in range(0, NbVertices)]
    Marked = [0 for j in range(0, NbVertices)]
    Chain = []
    Temp = []

    return {'temp': Temp, 'Phi': Phi, 'Flow': Flow, 'Color': Color, 'Color_succ': Color_succ, 'Color_prec': Color_prec, 'Chain': Chain,
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


def UpdateColorMinCost(infoOrigDestCptyCost, infoSuccPrec, infoColor):

    Origine = infoOrigDestCptyCost['orig']
    Destination = infoOrigDestCptyCost['dest']
    MaxCapacity = infoOrigDestCptyCost['maxCpty']
    MinCapacity = infoOrigDestCptyCost['minCpty']
    Cost = infoOrigDestCptyCost['cost']
    # Phi = infoColor['Phi']

    succ = infoSuccPrec['succ']
    prec = infoSuccPrec['prec']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    for u in range(0, NbArcs):
        i = Origine[u]
        j = Destination[u]
        if infoColor['Phi'][u] < Cost[u]:
            if infoColor['Flow'][u] > MinCapacity[u]:
                infoColor['Color'][u] = 'V'
            if infoColor['Flow'][u] < MinCapacity[u]:
                infoColor['Color'][u] = 'N'
            if infoColor['Flow'][u] == MinCapacity[u]:
                infoColor['Color'][u] = 'I'
        if infoColor['Phi'][u] > Cost[u]:
            if infoColor['Flow'][u] > MaxCapacity[u]:
                infoColor['Color'][u] = 'V'
            if infoColor['Flow'][u] < MaxCapacity[u]:
                infoColor['Color'][u] = 'N'
            if infoColor['Flow'][u] == MaxCapacity[u]:
                infoColor['Color'][u] = 'I'
        if infoColor['Phi'][u] == Cost[u]:
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


def UpdateTension(infoOrigDestCptyCost, infoColor, infoOmega):

    MaxCapacity = infoOrigDestCptyCost['maxCpty']
    MinCapacity = infoOrigDestCptyCost['minCpty']
    Cost = infoOrigDestCptyCost['cost']
    # Phi = infoColor['Phi']

    op = infoOmega['OmegaPlus']
    om = infoOmega['OmegaMoins']

    episilon = 99999
    infoColor['temp'] = []
    for i in (op + om):
        if i in op:
            if infoColor['Flow'][i] == MaxCapacity[i]:
                infoColor['temp'].append(99999)
            else:
                infoColor['temp'].append(Cost[i] - infoColor['Phi'][i])
        elif i in om:
            if infoColor['Flow'][i] == MinCapacity[i] and infoColor['Phi'][i] <= Cost[i]:
                infoColor['temp'].append(99999)
            else:
                infoColor['temp'].append(infoColor['Phi'][i] - Cost[i])
    episilon = min(infoColor['temp'])

    for i in (op + om):
        if i in op:
            infoColor['Phi'][i] += episilon
        if i in om:
            infoColor['Phi'][i] -= episilon

    return infoColor
