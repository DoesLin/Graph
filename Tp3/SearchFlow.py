import ReadGraph
import SearchChain
import UpdateFlow


def SearchSetA(Marked, NbVertices):

    SetA = []

    for i in range(0, NbVertices):
        if Marked[i] == 1:
            SetA.append(i)

    return SetA


def SearchSetA_ts(infoOrigDestCpty, infoSuccPrec, infoColor, u0):

    Origine = infoOrigDestCpty['orig']
    Destination = infoOrigDestCpty['dest']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    # NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']
    succ = infoSuccPrec['succ']
    prec = infoSuccPrec['prec']

    SetA = []
    Liste = []
    dep = Destination[u0]
    # print 'dest u0 = ', dep
    arr = Origine[u0]
    Liste.append(dep)
    SetA.append(dep)
    Deja_emplie = [0] * NbVertices
    Marque = [0 for j in range(0, NbVertices)]
    while (Liste != []):
        i = Liste[0]
        Marque[i] = 1
        del (Liste[0])
        for s in succ[i]:
            if s != arr and Marque[s] == 0 and Deja_emplie[s] == 0:
                if infoColor['Color'][u0] == 'N':
                    if infoColor['Color_succ'][i][succ[i].index(
                            s)] == 'N' or infoColor['Color_succ'][i][succ[i].index(
                                s)] == 'R':
                        Liste = [s] + Liste
                        SetA.append(s)
                        Deja_emplie[s] = 1
                elif infoColor['Color'][u0] == 'V':
                    if infoColor['Color_succ'][i][succ[i].index(
                            s)] == 'V' or infoColor['Color_succ'][i][succ[i].index(
                                s)] == 'R':
                        Liste = [s] + Liste
                        SetA.append(s)
                        Deja_emplie[s] = 1
        for d in prec[i]:
            if d != arr and Marque[d] == 0 and Deja_emplie[d] == 0:
                if infoColor['Color'][u0] == 'N':
                    if infoColor['Color_prec'][i][prec[i].index(
                            d)] == 'V' or infoColor['Color_prec'][i][prec[i].index(
                                d)] == 'R':
                        Liste = [d] + Liste
                        SetA.append(d)
                        Deja_emplie[d] = 1
                elif infoColor['Color'][u0] == 'V':
                    if infoColor['Color_prec'][i][prec[i].index(
                            d)] == 'N' or infoColor['Color_prec'][i][prec[i].index(
                                d)] == 'R':
                        Liste = [d] + Liste
                        SetA.append(d)
                        Deja_emplie[d] = 1

    return SetA


def SearchOmega(Origine, Destination, SetA):

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    OmegaPlus = []
    OmegaMoins = []

    for i in range(0, NbArcs):
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
        infoOmega = SearchOmega(Origine, Destination, setA)
        wp = sum(MaxCapacity[i] for i in infoOmega['OmegaPlus'])
        wm = sum(MinCapacity[i] for i in infoOmega['OmegaMoins'])
        # print('OmegaPlus:', infoOmega['OmegaPlus'],
        #       'OmegaMoins: ', infoOmega['OmegaMoins'])
        # print(setA)
        # print(wp, wm)
        if wp - wm <= 0:
            print("Il n'existe pas de flot compatible!")
        return{'FeasibleFlow': FeasibleFlow, 'SetA': setA, 'Omega': infoOmega}

    return{'FeasibleFlow': FeasibleFlow, 'Compatible': Compatible, 'Flow': infoColor['Flow']}


def SearchMinCostFlow(infoOrigDestCptyCost, infoSuccPrec, infoColor):

    Origine = infoOrigDestCptyCost['orig']
    Destination = infoOrigDestCptyCost['dest']
    MaxCapacity = infoOrigDestCptyCost['maxCpty']
    MinCapacity = infoOrigDestCptyCost['minCpty']
    Cost = infoOrigDestCptyCost['cost']

    # succ = infoSuccPrec['succ']
    # prec = infoSuccPrec['prec']

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    # NbVertices = infoNbArcVert['NbVertices']

    Conforme = [0] * NbArcs

    infoColor = UpdateFlow.UpdateColorMinCost(
        infoOrigDestCptyCost, infoSuccPrec, infoColor)
    for i in range(0, NbArcs):
        if infoColor['Phi'][i] == Cost[i] and (infoColor['Flow'][i] in range(MinCapacity[i],
                                                                             MaxCapacity[i] + 1)):
            Conforme[i] = 1
        elif infoColor['Phi'][i] > Cost[i] and infoColor['Flow'][i] == MaxCapacity[i]:
            Conforme[i] = 1
        elif infoColor['Phi'][i] < Cost[i] and infoColor['Flow'][i] == MinCapacity[i]:
            Conforme[i] = 1
        else:
            Conforme[i] = 0
    NbConforme = sum(Conforme)
    print('Updated')
    print('Conform: ', Conforme)
    print('Flow: ', infoColor['Flow'])
    print('Phi: ', infoColor['Phi'])

    while NbConforme != NbArcs:
        u0 = Conforme.index(0)

        resultChainColor = SearchChain.SearchChainColor(
            infoOrigDestCptyCost, infoSuccPrec, infoColor, u0)
        if resultChainColor['result']:
            infoColor = UpdateFlow.UpdateFlow(infoOrigDestCptyCost,
                                              infoSuccPrec, infoColor)
        else:
            setA = SearchSetA_ts(infoOrigDestCptyCost,
                                 infoSuccPrec, infoColor, u0)
            infoOmega = SearchOmega(Origine, Destination, setA)
            # ChercheSetA(u0)
            # ChercheOmega(setA)

            if infoColor['Color'][u0] == 'V':
                infoColor['temp'] = infoOmega['OmegaPlus']
                infoOmega['OmegaPlus'] = infoOmega['OmegaMoins']
                infoOmega['OmegaMoins'] = infoColor['temp']
            print('Updated')
            print('setA:', setA)
            print('Color: ', infoColor['Color'])
            # print('o+:', infoOmega['OmegaPlus'])
            # print('o-:', infoOmega['OmegaMoins'])

            infoColor = UpdateFlow.UpdateTension(
                infoOrigDestCptyCost, infoColor, infoOmega)

        infoColor = UpdateFlow.UpdateColorMinCost(
            infoOrigDestCptyCost, infoSuccPrec, infoColor)

        for i in range(0, NbArcs):
            if infoColor['Phi'][i] == Cost[i] and (infoColor['Flow'][i] in range(MinCapacity[i],
                                                                                 MaxCapacity[i] + 1)):
                Conforme[i] = 1
            elif infoColor['Phi'][i] > Cost[i] and infoColor['Flow'][i] == MaxCapacity[i]:
                Conforme[i] = 1
            elif infoColor['Phi'][i] < Cost[i] and infoColor['Flow'][i] == MinCapacity[i]:
                Conforme[i] = 1
            else:
                Conforme[i] = 0
        NbConforme = sum(Conforme)
        print('Updated')
        print('Conform: ', Conforme)
        print('Flow: ', infoColor['Flow'])
        print('Phi: ', infoColor['Phi'])

    # print('Flow: ', infoColor['Flow'])
    # print('Phi: ', infoColor['Phi'])
    return {'Flow': infoColor['Flow'], 'Phi': infoColor['Phi'], 'Color': infoColor['Color']}
