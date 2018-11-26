import ReadGraph
import SearchChain


def main():
    file_graph = './Tp1/graph_TP1.txt'

    all_arcs = ReadGraph.readGraph(file_graph)
    # print(all_arcs)

    # Graphe 1
    infoOrigDest = ReadGraph.getOrigDest(all_arcs)

    NbArcs = len(infoOrigDest['orig'])
    NbVertices = max(max(infoOrigDest['orig']), max(infoOrigDest['dest']))+1
    # print(NbArcs)
    # print(NbVertices)

    # Graphe 2
    Origine2 = [0, 1, 1, 2, 2, 3, 3]
    Destination2 = [1, 2, 3, 0, 3, 0, 2]

    infoSuccPrec = ReadGraph.getSuccPrec(Origine2, Destination2)
    # print(infoSuccPrec['succ'])
    # print(infoSuccPrec['numsucc'])
    # print(infoSuccPrec['prec'])
    # print(infoSuccPrec['numprec'])

    # Graphe 3
    ##Origine3 = [0, 1]
    ##Destination3 = [1, 2]
    Origine3 = [0, 1, 1, 2, 2, 3, 3]
    Destination3 = [1, 2, 3, 0, 3, 0, 2]

    infoABSuccPrec = ReadGraph.getABSuccPrec(Origine3, Destination3)
    # print("Verifier _aprec")
    # print(infoABSuccPrec['_aprec'])
    # print(infoABSuccPrec['_bprec'])

    # print("Verifier _asucc")
    # print(infoABSuccPrec['_asucc'])
    # print(infoABSuccPrec['_bsucc'])

    dep = 1
    arr = 2
    resultSearchChain = SearchChain.SearchChain(
        Origine3, Destination3, dep, arr)
    # print(resultSearchChain['result'])
    # print(resultSearchChain['Predecessor'])
    # print(resultSearchChain['Successor'])

    u0 = 1
    resultSearchChainTs = SearchChain.SearchChain_ts(
        Origine3, Destination3, u0)
    # print(resultSearchChainTs['result'])
    # print(resultSearchChainTs['Predecessor'])
    # print(resultSearchChainTs['Successor'])

    # resultChain = SearchChain.IdentifyChain(Origine3, Destination3, dep, arr)
    resultChainTs = SearchChain.IdentifyChain_ts(Origine3, Destination3, u0)
    if resultChainTs != False:
        print(resultChainTs['The_chain'])
        print(resultChainTs['mu_plus'])
        print(resultChainTs['mu_minus'])


if __name__ == '__main__':
    main()
