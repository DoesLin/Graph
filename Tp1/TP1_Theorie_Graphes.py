# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrateur
#
# Created:     16/11/2018
# Copyright:   (c) Administrateur 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os

file_graph = './Tp1/graph_TP1.txt'


TheGraph = open(file_graph, 'r')
all_arcs = TheGraph.readlines()
TheGraph.close()

print(all_arcs)

# Graphe 1
Origine = []
Destination = []
for one_arc in all_arcs:
    this_arc = one_arc.split("\t")
    orig = int(this_arc[0])
    dest = int(this_arc[1].strip("\n"))
    Origine.append(orig)
    Destination.append(dest)

NbArcs = len(Origine)
NbVertices = max(max(Origine), max(Destination))+1

print(NbArcs)
print(NbVertices)

# Graphe 2
Origine2 = [0, 1, 1, 2, 2, 3, 3]
Destination2 = [1, 2, 3, 0, 3, 0, 2]

NbArcs2 = len(Origine2)
NbVertices2 = max(max(Origine2), max(Destination2))+1

# la liste des successeurs de i
# succ = new [len(NbVertices2)][] en java
succ = [[] for i in range(NbVertices2)]
# NumÃ©ro de l'arc successeur de i
numsucc = [[] for i in range(NbVertices2)]
# NumÃ©ro des arcs prÃ©cedents
numprec = [[] for i in range(NbVertices2)]
# la liste des pÃ©dÃ©cesseurs de i
prec = [[] for i in range(NbVertices2)]

for u in range(0, NbArcs2):
    i = Origine2[u]
    j = Destination2[u]
    succ[i].append(j)
    numsucc[i].append(u)
    prec[j].append(i)
    numprec[j].append(u)


print(succ)
print(numsucc)
print(prec)
print(numprec)


# la liste des successeurs

a_succ = []
b_succ = []

curB = 0
a_succ.append(curB)
for s in succ:
    b_succ = b_succ + s
    curB = curB + len(s)
    a_succ.append(curB)

print("test a & b")
print(a_succ)
print(b_succ)

a_prec = []
b_prec = []

curB = 0
a_prec.append(curB)
for p in prec:
    b_prec = b_prec + p
    curB = curB + len(p)
    a_prec.append(curB)

print(a_prec)
print(b_prec)

Marked = [False for j in range(0, NbVertices2)]
Predecessor = [-1 for j in range(0, NbVertices2)]
Successor = [-1 for j in range(0, NbVertices2)]


def SearchChain(dep, arr):
    global Marked
    In_Stack = [False for j in range(0, NbVertices2)]
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

    return Found


print(SearchChain(0, 3))
print(Predecessor)
print(Successor)

# Graphe 3
##Origine3 = [0, 1]
##Destination3 = [1, 2]
Origine3 = [0, 1, 1, 2, 2, 3, 3]
Destination3 = [1, 2, 3, 0, 3, 0, 2]

NbArcs3 = len(Origine3)
NbVertices3 = max(max(Origine3), max(Destination3))+1

# la liste des successeurs de i
# succ = new [len(NbVertices2)][] en java
succ = [[] for i in range(NbVertices3)]
# NumÃ©ro de l'arc successeur de i
numsucc = [[] for i in range(NbVertices3)]
# NumÃ©ro des arcs prÃ©cedents
numprec = [[] for i in range(NbVertices3)]
# la liste des pÃ©dÃ©cesseurs de i
prec = [[] for i in range(NbVertices3)]

for u in range(0, NbArcs3):
    i = Origine3[u]
    j = Destination3[u]
    succ[i].append(j)
    numsucc[i].append(u)
    prec[j].append(i)
    numprec[j].append(u)


# Definition
_asucc = []
_bsucc = []
_nsucc = []
_inds = 0

for j in range(0, NbVertices3):
    _asucc.append(_inds)
    _inds = _inds + len(succ[j])
    _bsucc = _bsucc + succ[j]
    _nsucc = numsucc + numsucc[j]
_asucc.append(_inds)


print("Verifier _asucc")
print(_asucc)
print(_bsucc)

_aprec = []
_bprec = []
_nprec = []
_inds = 0

for j in range(0, NbVertices3):
    _aprec.append(_inds)
    _inds = _inds + len(prec[j])
    _bprec = _bprec + prec[j]
    _nprec = numprec + numprec[j]
_aprec.append(_inds)

print("Verifier _aprec")
print(_aprec)
print(_bprec)

Marked = [False for j in range(0, NbVertices3)]


def SearchChain_ts(u0):
    global Marked
    arr = Origine3[u0]
    dep = Destination3[u0]

    Predecessor = [-1 for j in range(0, NbVertices3)]
    Successor = [-1 for j in range(0, NbVertices3)]
    In_Stack = [False for j in range(0, NbVertices3)]

    List = []
    List.append(dep)
    Found = False

    while(List != [] and not Found):
        i = List[0]
        del(List[0])
        Marked[i] = True
# for k in succ[j] :
        for j in range(_asucc[i], _asucc[i+1]):
            the_succ = _bsucc[_asucc[i]+j]
            the_arc = _nsucc[_asucc[i]+j]

            if (the_succ == arr):
                Found = True
            if(not In_Stack[the_succ]):
                List.append(the_succ)
                In_Stack[the_succ] = True
                Predecessor[the_succ] = i

        for j in range(_aprec[i], _aprec[i+1]):
            the_prec = _bprec[_bprec[i]+j]
            the_arc = _nprec[_aprec[i]+j]

            if (the_prec == arr):
                Found = True
            if(not In_Stack[the_prec]):
                List.append(the_prec)
                In_Stack[the_prec] = True
                Successor[the_prec] = i

    return Found


print("test search_ts")
print(SearchChain_ts(1))
print(Predecessor)
print(Successor)
# print(SearchChain_ts(2))
# print(Predecessor)
# print(Successor)
