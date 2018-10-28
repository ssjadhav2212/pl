from operation import operation
#goal_stack is actual stack implemented by list to save current operation state
goal_stack = []

#actual blocks stores unique blocks used. One can use even numbers to name blocks
actual_blocks = ['A','B','C','D']

#stores blocks on which we cannot place other block reason being that block is expected to carry some other block
blocks_cannot_be_stacked = []

#if goal state contains ontable thingy then this flag forcefully keeps block on table even if there is block available which can carry block without worry
ontable_flag = False


#stores sequence of stack and unstack operations in LIFO
operation_stack = []

#utility function to identify which goal states are fulfilled in initial state
def initiate(initial_state, goal_state, stack_pointer):
    print('initial state is : ',initial_state)
    print()
    print('goal state is : ',goal_state)
    print()
    Istates = initial_state.split('^')
    Gstates = goal_state.split('^')
    true_sub_goals = []
    for entry in Gstates:
        if entry not in Istates:
            print(entry)
            oper = entry.split('(')[0]
            opd = entry.split('(')[1].split(')')
            print('opd = ',opd)
            print(len(opd[0].split(',')))
            if len(opd[0].split(','))== 1:
                obj = operation(oper,opd[0],'')
                goal_stack.insert(stack_pointer,obj)
                stack_pointer+=1
            else:
                obj = operation(oper,opd[0].split(',')[0],opd[0].split(',')[1])
                goal_stack.insert(stack_pointer, obj)
                stack_pointer += 1
        else:
            true_sub_goals.append(entry)
    print('-----------------------------------------')
    print('true sub-goals are: ')
    for item in true_sub_goals:
        print(item)
    print('-----------------------------------------')
    '''for obj in goal_stack:
        print(obj.op_name,end='')
        print(obj.operand1,end='')
        print(obj.operand2)'''
    return stack_pointer


#utility function which returns pre-conditions which must be true to carry out operation
def return_pre_conditions(goal):
    list_of_pre = []
    if goal.op_name == 'ON':
        obj = operation('STACK',goal.operand2,goal.operand1)
        operation_stack.insert(0,"stack")
        list_of_pre.append(obj)
        blocks_cannot_be_stacked.append(goal.operand1)
        blocks_cannot_be_stacked.append(goal.operand2)
        return list_of_pre

    elif goal.op_name == 'STACK':

        obj2 = operation('HOLD',goal.operand2,'')
        list_of_pre.insert(0,obj2)
        obj1 = operation('CLEAR', goal.operand1, '')
        list_of_pre.insert(1, obj1)
        return list_of_pre

    elif goal.op_name == "UNSTACK":

        obj = operation("CLEAR", goal.operand2, '')
        list_of_pre.insert(0, obj)
        obj = operation("IFON",goal.operand1,goal.operand2)
        list_of_pre.insert(1,obj)
        return list_of_pre

#returns answer True/False for atomic conditions
def return_answer(goal,current_state):

    if goal.op_name == 'CLEAR':
        print('entered clear and current state is = and to check is = ',current_state,goal.operand1)
        states  = current_state.split('^')
        for s in states:
            #print('s = ',s)
            if "ON(" in s :
                elements = s.split(',')
                if elements[1][0] == goal.operand1:
                    return True
        return False
    elif goal.op_name == 'HOLD':
        return HOLD == ''
    elif goal.op_name == "IFON":
        to_find = "ON("+goal.operand2+","+goal.operand1+")"
        if to_find in current_state:
            return True
        return False

    elif goal.op_name == "ONTABLE":
        sttr = "ONTABLE("+goal.operand1+")"
        if sttr in current_state:
            return True
        return False


#returns block residing above given block
def return_above_block(goal,current_state):
    states  = current_state.split('^')
    for s in states:
            #print('s = ',s)
            if "ON(" in s :
                elements = s.split(',')
                if elements[1][0] == goal.operand1:
                    return (elements[0][len(elements[0])-1])

#returns block residing below given block
def return_block_below(goal,current_state):
    states = current_state.split('^')
    for s in states:
        # print('s = ',s)
        if "ON(" in s:
            elements = s.split(',')
            if elements[0][len(elements[0])-1] == goal.operand1:
                return elements[1][0]


if __name__ == "__main__":
    stack_pointer = 0
    initial_state = 'ON(B,A)^ONTABLE(C)^ONTABLE(A)^ONTABLE(D)'
    #input('enter initial state as string')
    goal_state = 'ON(C,A)^ON(B,D)^ONTABLE(A)^ONTABLE(D)'
    #input('enter goal state as string')
    stack_pointer = initiate(initial_state,goal_state,stack_pointer)
    print('stack pointer! = ', stack_pointer)
    current_state = initial_state
    print("current_state = ",initial_state)
    #for every unachieved subgoal there are some pre-conditions which must hold true
    HOLD = ''
    for unachieved_goal in goal_stack:
        print("***********************************")
        print('goal information is:')
        print('operation = ', unachieved_goal.op_name)
        print('operand1 = ', unachieved_goal.operand1)
        print('operand2 = ', unachieved_goal.operand2)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

    while len(goal_stack) != 0:
        #unachieved goal is popped from goal_stack
        unachieved_goal = goal_stack.pop(0)


        print("***********************************")
        print('goal information is:')
        print('operation = ',unachieved_goal.op_name)
        print('operand1 = ',unachieved_goal.operand1)
        print('operand2 = ', unachieved_goal.operand2)

        #if condition checks whether operation is atomic or not. If not atomic it fetches pre-conditions and add them into stack
        if unachieved_goal.op_name  not in ['ARMEMPTY','CLEAR','HOLD',"IFON","ONTABLE"]:

            precons = return_pre_conditions(unachieved_goal)
            if precons != None:
                for condition in precons:
                    goal_stack.insert(0,condition)


        else:   #check for atomic conditions
            if unachieved_goal.op_name == "ONTABLE":
                value = return_answer(unachieved_goal,current_state)
                if not value:
                    block_below=return_block_below(unachieved_goal,current_state)
                    ontable_flag = True
                    obj = operation("UNSTACK",block_below,unachieved_goal.operand1)
                    goal_stack.insert(0,obj)
                    operation_stack.insert(0,"unstack")
                    continue

            if len(operation_stack)>0 and operation_stack[0] == "stack":

                #since stack operation to perform I already know sequence of pre-conditions
                #1)The block on which you will put another block must be clear first
                print('in stacking at start op = ',unachieved_goal.op_name,"and operand = ",unachieved_goal.operand1)
                value = return_answer(unachieved_goal, current_state)
                temp_obj = unachieved_goal

                if value :

                        operand2 = return_above_block(unachieved_goal, current_state)
                        obj = operation("UNSTACK", unachieved_goal.operand1, operand2)
                        operation_stack.insert(0,"unstack")
                        #goal_stack.insert(0,temp_obj)
                        goal_stack.insert(0,unachieved_goal)
                        goal_stack.insert(0, obj)

                else:
                    print('block is clear @ ',unachieved_goal.operand1)
                    clrblk = unachieved_goal.operand1
                    unachieved_goal = goal_stack.pop(0)
                    #value = return_answer(unachieved_goal, current_state)
                    print('HOLD %%%= ',HOLD)
                    if  HOLD == unachieved_goal.operand1:
                            #do actual stacking
                            if "ONTABLE("+HOLD+")" in current_state:
                                current_state = current_state.replace("ONTABLE("+HOLD+")",'')
                            current_state += '^ON('+unachieved_goal.operand1+","+clrblk+")"
                            print('modified state by stacking is now = ',current_state)
                            HOLD = ''
                            operation_stack.pop(0)
                    else:
                            if HOLD == '':
                                print('HOLD khaali hai')
                                print('junior = ',unachieved_goal.operand1)
                                check = operation("CLEAR",unachieved_goal.operand1,'')
                                ans = return_answer(check,current_state)
                                if ans:
                                    print('junior mein akad hai')
                                    blk = return_above_block(check,current_state)
                                    print('temp_obj ka op = ',temp_obj.op_name)
                                    #exit(0)
                                    goal_stack.insert(0, unachieved_goal)
                                    goal_stack.insert(0, temp_obj)
                                    obj = operation("UNSTACK",check.operand1,blk)
                                    goal_stack.insert(0,obj)
                                    operation_stack.insert(0,"unstack")
                                else:

                                    print('junior achha hai yaar')
                                    HOLD = unachieved_goal.operand1

                                    if "ONTABLE(" + HOLD + ")" in current_state:
                                        current_state = current_state.replace("ONTABLE(" + HOLD + ")", '')
                                    else:
                                        #anns = is_present_on_something(HOLD,current_state)
                                        #if anns:
                                            blk_blw = return_block_below(operation("NO EFFECT",unachieved_goal.operand1,''),current_state)
                                            current_state = current_state.replace('ON('+HOLD+","+blk_blw+")",'')
                                    current_state += '^ON(' + unachieved_goal.operand1 + "," + clrblk + ")"
                                    print('modified state by stacking is now = ', current_state)
                                    HOLD = ''
                                    operation_stack.pop(0)



                            else:
                                    print('HOLD mein koi DUSRA hai')


                                    print('currently value of HOLD is = ',HOLD,"which is unwanted")
                                    j = -1

                                    for block in actual_blocks:
                                            if block not in blocks_cannot_be_stacked:

                                                if block!= HOLD and not return_answer(operation("CLEAR",block,''),current_state):
                                                    j = block
                                                    break
                                    if j!= -1:
                                        obj = operation("STACK",j,HOLD)
                                        print('newly found block = ',j)
                                        operation_stack.insert(0,"stack")
                                        print("unacg op = ",unachieved_goal.op_name)

                                        print('temp_obj ka op = ', temp_obj.op_name)

                                        goal_stack.insert(0, unachieved_goal)
                                        goal_stack.insert(0, temp_obj)
                                        goal_stack.insert(0,obj)
                                    else:
                                        current_state+="ONTABLE("+HOLD+")"
                                        HOLD = ''
                                        goal_stack.insert(0, temp_obj)
                                        print('placed on table as no other block is available')


            elif len(operation_stack)>0 and operation_stack[0] == "unstack":

                print('unstack operation to checked')
                # since unstack operation to perform I already know sequence of pre-conditions
                # 1)The block on which you remove must be present on  first
                value = return_answer(unachieved_goal, current_state)
                string_to_remove = 'ON('+unachieved_goal.operand2+","+unachieved_goal.operand1+")"
                tohld = unachieved_goal.operand2
                ty = ''
                temp_obj = unachieved_goal
                print('string t remove = ',string_to_remove)
                if value:
                    unachieved_goal = goal_stack.pop(0)
                    print('in unstacking second layer operation = ',unachieved_goal.op_name)
                    value = return_answer(unachieved_goal, current_state)
                    print('value from clear = ',value)
                    if value:
                        pass
                    else:
                        if HOLD == '':
                            #no issue
                            HOLD = unachieved_goal.operand1
                            print('HOLD@@@ = ',HOLD)
                            current_state = current_state.replace(string_to_remove, '')
                            splits = current_state.split('^')
                            current_state = ''
                            for i in splits:
                                if len(i) > 0:
                                    current_state += i + '^'
                            current_state = current_state[:len(current_state) - 1]

                            if ontable_flag:
                                current_state += "^ONTABLE(" + HOLD + ")"
                                HOLD = ''
                                ontable_flag = False

                            print('placed on table as it is expected')
                            print('unstacked bro and final current_state is = ', current_state)
                            operation_stack.pop(0)


                        else:
                            #HOLD contains something
                            goal_stack.insert(0,temp_obj)
                            goal_stack.insert(0,unachieved_goal)
                            print('Current unwanted value of HOLD in UNSTACK is = ',HOLD)
                            j = ''
                            if not ontable_flag:
                                for block in actual_blocks:
                                    if block not in blocks_cannot_be_stacked:

                                        if block != HOLD and not return_answer(operation("CLEAR", block, ''),
                                                                               current_state):
                                            j = block
                                            break
                            if j != '':
                                obj = operation("STACK", j, HOLD)
                                print('newly found block = ', j)
                                operation_stack.insert(0, "stack")
                                goal_stack.insert(0,unachieved_goal)
                                goal_stack.insert(0, temp_obj)

                                goal_stack.insert(0, obj)
                            else:
                                current_state += "ONTABLE(" + HOLD + ")"
                                HOLD = ''
                                goal_stack.insert(0, temp_obj)
                                print('placed on table as no other block is available')
