
#import queue as Q


class Node:
    def __init__(self,id,distance):
        self.id = id;
        self.distance=distance

    def __lt__(self, other):
        return self.distance < other.distance


if __name__=="__main__":
    n = int(input("Enter total number of nodes"))
    print('Nodes will be numbered as 1 to ', n)

    print('Enter graph')

    Graph = []


    '''for i in range(1,n+1):
        current = []
        for j in range(1,n+1):
            val = input()
            current.append(val)

        Graph.append(current)
        print('row appended')'''

    # currently hard coded graph for debugging purpose uncomment above code  and comment below code to take graph as per your choice
    Graph = [
        [0,1,1,1,0,0,0,0,0,0,0,0,0,0], #1
        [1,0,0,0,1,1,0,0,0,0,0,0,0,0],#2
        [1,0,0,0,0,0,1,1,0,0,0,0,0,0],#3
        [1,0,0,0,0,0,0,0,1,0,0,0,0,0],#4
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0],#5
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0],#6
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0],#7
        [0,0,1,0,0,0,0,0,0,0,0,0,0,0],#8
        [0,0,0,1,0,0,0,0,0,1,1,0,0,0],#9
        [0,0,0,0,0,0,0,0,1,0,0,1,1,1],#10
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,],#11
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0],#12
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0],#13
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0]#14

    ]

    start = int(input('Enter any number between 1 to N as start node'))

    goal = int(input('Enter any number between 1 to N as goal node'))

    print('enter heuristic value for every node from 1 to N')


    #values are currently hard-coded for debugging purpose uncomment below code to take input
    heuristic = [0,3,6,5,9,8,12,14,7,5,6,1,10,2]

    '''for i in range(0,n):
        heu = int(input())
        heuristic.append(heu)'''




    source = Node(start,heuristic[start-1])

    visited = []
    for i in range(0,n):
        x=False
        visited.append(x)

    PQ = PriorityQueue()
    PQ.put(source)
    visited[start-1]=True

    parents =[]

    for i in range(0,n):
        parents.append(-1)



    while(not PQ.empty()):
        minNode = PQ.get()


        if minNode.id == goal:
            print(minNode.id)
            print('=====Search completed=====')
        else:
            nodeList = Graph[minNode.id-1]
            for i in range(0,n):
                if nodeList[i]==1 and visited[i]==False:
                    visited[i]=True
                    PQ.put(Node(i+1,heuristic[i]))
                    parents[i]= minNode.id



    print('PATH to GOAL is :-')
    i=goal-1
    print(goal,"===>","\n")
    while(parents[i]!=-1):
        print(parents[i],"===>","\n")
        i=parents[i]-1
        #print('new  i = ',i)




    '''for i in range(0,n):
        print(parents[i],"\n")'''








