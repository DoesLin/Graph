import ReadGraph
import SearchChain
import UpdateFlow


def main():
    file_graph = './Tp2/graph_TP2.txt'

    all_arcs = ReadGraph.readGraph(file_graph)
    # print(all_arcs)

    # Graphe 1
    infoOrigDestCpty = ReadGraph.getOrigDestCpty(all_arcs)
    # print(infoOrigDestCpty['orig'])
    # print(infoOrigDestCpty['dest'])
    # print(infoOrigDestCpty['maxCpty'])
    # print(infoOrigDestCpty['minCpty'])

    Origine = infoOrigDestCpty['orig']
    Destination = infoOrigDestCpty['dest']
    infoSuccPrec = ReadGraph.getSuccPrec(Origine, Destination)
    # print(infoSuccPrec['succ'])
    # print(infoSuccPrec['numsucc'])
    # print(infoSuccPrec['prec'])
    # print(infoSuccPrec['numprec'])

    infoABSuccPrec = ReadGraph.getABSuccPrec(Origine, Destination)
    # print("Verifier _aprec")
    # print(infoABSuccPrec['_aprec'])
    # print(infoABSuccPrec['_bprec'])
    # print(infoABSuccPrec['_nprec'])

    # print("Verifier _asucc")
    # print(infoABSuccPrec['_asucc'])
    # print(infoABSuccPrec['_bsucc'])
    # print(infoABSuccPrec['_nsucc'])

    infoNbArcVert = ReadGraph.getNbArcVert(Origine, Destination)
    NbArcs = infoNbArcVert['NbArcs']
    NbVertices = infoNbArcVert['NbVertices']

    Flow = [0] * NbArcs
    Color = ['-' for j in range(0, NbArcs)]
    Color_succ = [[] for i in range(NbVertices)]
    Color_prec = [[] for i in range(NbVertices)]
    Distance = []
    The_Chain = []

    testU = 0
    UpdateFlow.UpdateColor(infoOrigDestCpty, Flow, Color,
                           Color_succ, Color_prec, testU)


if __name__ == '__main__':
    main()
