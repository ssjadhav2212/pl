from ListNode import ListNode

def return_minimum_value_node(openList):
    min = 100000
    min_node=openList[0]
    for node in openList:
        if node.f<min:
            min = node.f
            min_node=node
    return min_node

if __name__ == "__main__":
    n = int(input("Enter total number of nodes"))
    print('Nodes will be numbered as 1 to ',n)

    print('Enter graph')

    Graph = []

    total_nodes = []
    for i in range(1,n+1):
        total_nodes.append(i)


    '''for i in range(1,n+1):
        current = []
        for j in range(1,n+1):
            val = input()
            current.append(val)

        Graph.append(current)
        print('row appended')'''



    #currently hard coded graph for debugging purpose uncomment above code  and comment below code to take graph as per your choice
    Graph=[
       [ 0 ,1,-1 ,4,-1],
         [-1, 0, 5, 2, 12],
         [ -1, -1, 0 ,-1, 3],
          [-1,-1, 2, 0 ,-1],
          [-1,-1,-1,-1, 0]

    ]


    start = int(input('Enter any number between 1 to N as start node'))

    print('enter heuristic value for every node from 1 to N')

    heuristic = []

    for i in range(1,n+1):
         heu = int(input())
         dict = {i:heu}
         heuristic.append(dict)


    OPEN = []

    heu_val = heuristic[start-1];

    heu_val = heu_val[start]

    #print('heu val of start = ',heu_val)

    empty = []



    start_node = ListNode(empty,start,0,heu_val)

    OPEN.append(start_node)

    while len(OPEN)>0:
        current_node = return_minimum_value_node(OPEN)

        OPEN.remove(current_node)
        print('***********************************************')
        print('currently minimal node with value of f as  = ',current_node.f)

        if current_node.is_Goal(n):
            print('CURRENT STATE IS GOAL STATE')
            print('optimal value is = ',current_node.f)

            for i in current_node.node_list:
                print(i,"\n")
            break
        else:
            #for every successor
            print('current minimal node is not goal node')
            adjacent_nodes = Graph[current_node.ID-1]
            cnt = 0
            for i in adjacent_nodes:

                if i != -1 and i!=0:
                    print('current node = ',current_node.ID,' and successor = ',cnt+1)
                    heu_val = heuristic[cnt]
                    heu_val = heu_val[cnt+1]
                    successor_node = ListNode(current_node.node_list,cnt+1,current_node.g+i,heu_val)
                    OPEN.append(successor_node)
                cnt+=1




'''
0 1 -1 4 -1
-1 0 5 2 12
-1 -1 0 -1 3
-1 -1 2 0 -1
-1 -1 -1 -1 0
'''