import ReadGraph
import SearchChain
import UpdateFlow
import SearchFlow


def main():
    # file_graph = './Tp3/graphe_TP3.txt'
    file_graph = './Tp3/graph_test4.txt'
    # file_graph = 'graphe_TP3.txt'

    all_arcs = ReadGraph.readGraph(file_graph)
    # print(all_arcs)

    # Graphe 1
    infoOrigDestCptyCost = ReadGraph.getOrigDestCptyCost(all_arcs)
    # print(infoOrigDestCptyCost['orig'])
    # print(infoOrigDestCptyCost['dest'])
    # print(infoOrigDestCptyCost['maxCpty'])
    # print(infoOrigDestCptyCost['minCpty'])
    # print(infoOrigDestCptyCost['cost'])

    Origine = infoOrigDestCptyCost['orig']
    Destination = infoOrigDestCptyCost['dest']
    infoSuccPrec = ReadGraph.getSuccPrec(Origine, Destination)
    infoColor = UpdateFlow.InitColor(Origine, Destination)
    # print(infoSuccPrec['succ'])
    # print(infoSuccPrec['prec'])
    # print(infoColor['Color_succ'])
    # print(infoColor['Color_prec'])

    resultMinCostFlow = SearchFlow.SearchMinCostFlow(
        infoOrigDestCptyCost, infoSuccPrec, infoColor)
    print(resultMinCostFlow)


if __name__ == '__main__':
    main()
