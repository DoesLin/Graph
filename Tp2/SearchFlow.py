import ReadGraph
import SearchChain
import UpdateFlow


def SearchSetA(Marked, NbVertices):

    SetA = []

    for i in range(0, NbVertices):
        if Marked[i] == 1:
            SetA.append(i)

    return SetA


def SearchOmega(Origine, Destination, infoColor, SetA):

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    OmegaPlus = []
    OmegaMoins = []

    for i in range(0, NbArcs):
        # if infoColor['Color'][i] == 'V':
        #     OmegaPlus.append(i)
        # if infoColor['Color'][i] == 'N':
        #     OmegaMoins.append(i)
        if Origine[i] in SetA and Destination[i] not in SetA:
            OmegaPlus.append(i)
        if Origine[i] not in SetA and Destination[i] in SetA:
            OmegaMoins.append(i)

    return {'OmegaPlus': OmegaPlus, 'OmegaMoins': OmegaMoins}


def SearchFeasibleFlow(infoOrigDestCpty, infoSuccPrec, infoColor):

    Origine = infoOrigDestCpty['orig']
    Destination = infoOrigDestCpty['dest']
    MaxCapacity = infoOrigDestCpty['maxCpty']
    MinCapacity = infoOrigDestCpty['minCpty']

    # succ = infoSuccPrec['succ']
    # prec = infoSuccPrec['prec']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    Compatible = [0] * NbArcs
    NbCompatible = sum(Compatible)
    FeasibleFlow = True

    while (NbCompatible != NbArcs and FeasibleFlow):
        u0 = Compatible.index(0)
        resultChainColor = SearchChain.SearchChainColor(
            infoOrigDestCpty, infoSuccPrec, infoColor, u0)
        if resultChainColor['result']:
            resultChainColor['infoColor'] = UpdateFlow.UpdateFlow(
                infoOrigDestCpty, infoSuccPrec, resultChainColor['infoColor'])
            resultChainColor['infoColor'] = UpdateFlow.UpdateColor(
                infoOrigDestCpty, infoSuccPrec, resultChainColor['infoColor'], u0)
            for u in range(0, NbArcs):
                if resultChainColor['infoColor']['Flow'][u] in range(MinCapacity[u], MaxCapacity[u] + 1):
                    Compatible[u] = 1
        else:
            FeasibleFlow = False
        NbCompatible = sum(Compatible)

    # print('FeasibleFlow: ', FeasibleFlow, '\nCompatible: ', Compatible)
    if NbCompatible != NbArcs:
        u0 = Compatible.index(0)
        setA = SearchSetA(infoColor['Marked'], NbVertices)
        # print(infoColor['Color'])
        infoOmega = SearchOmega(Origine, Destination, infoColor, setA)
        wp = sum(MaxCapacity[i] for i in infoOmega['OmegaPlus'])
        wm = sum(MinCapacity[i] for i in infoOmega['OmegaMoins'])
        print('OmegaPlus:', infoOmega['OmegaPlus'],
              'OmegaMoins: ', infoOmega['OmegaMoins'])
        # print(setA)
        print(wp, wm)
        if wp - wm <= 0:
            print("It doesn't exist feasible flow!")
        return{'FeasibleFlow': FeasibleFlow, 'SetA': setA, 'Omega': infoOmega}

    return{'FeasibleFlow': FeasibleFlow, 'Compatible': Compatible, 'Flow': infoColor['Flow']}
