from collections import namedtuple

to_write = []

creation_list = dict()
priority2_list = []
priority1_list = []
resource_holding = dict()
resource_available_waiting = dict()
PCB = namedtuple('PCB', 'PID status resource parent child priority')
RCB = namedtuple('RCB', 'aval waiting')
resource_wait = namedtuple('resource_wait', 'r_name amount')
resource_hold = namedtuple('resource_hold', 'p_name amount')
current_running = "init"

def set_up():
    resource_available_waiting["R1"] = RCB(aval = 1, waiting = [])
    resource_available_waiting["R2"] = RCB(aval = 2, waiting = [])
    resource_available_waiting["R3"] = RCB(aval = 3, waiting = [])
    resource_available_waiting["R4"] = RCB(aval = 4, waiting = [])


def print_creation_tree():
    for (x,y) in creation_list.items():
        print("\nThe process is: ", x, " status: ", y.status, " resource: ", y.resource, " parent: ", y.parent, " child: ", y.child, " priority: ", y.priority)
        

def print_priority():
    print("\nPriority 1: ", priority1_list)
    print("\nPriority 2: ", priority2_list)

def print_resource():
    for (x,y) in resource_holding.items():
        print("\nProcess holding resource is: ", x,)
        for i in y:
            print(" resource: ", i.p_name, " amount: ", i.amount)
    for (x,y) in resource_available_waiting.items():
        print("\nResource: ", x, " available: ", y.aval, " waiting list: ", y.waiting)

def resource_check(r_name, quantity):
    flag = 0
    if r_name == "R1" and (quantity > 1 or quantity <= 0):
        ##print("Resource R1 only has 1 resource: ERROR\n")
        flag = 1
    elif r_name == "R2" and (quantity <= 0 or quantity > 2):
        ##print("Resource R2 only has 2 resources: ERROR\n")
        flag = 1
    elif r_name == "R3" and (quantity <= 0 or quantity > 3):
        ##print("Resource R3 only has 3 resources: ERROR\n")
        flag = 1
    elif r_name == "R4" and (quantity <= 0 or quantity > 4):
        ##print("Resource R4 only has 4 resources: ERROR\n")
        flag = 1
    return flag
    
    
def scheduler():
    global current_running

    if len(priority2_list) != 0:
        if current_running != "init" and current_running in creation_list:
            creation_list[current_running] = creation_list[current_running]._replace(status = "waiting")
        priority2_list[0] = priority2_list[0]._replace(status = "running")
        
        if len(priority1_list) > 0:
            if current_running == priority1_list[0].PID:##a switch from p1 to p2
                priority1_list[0] = priority1_list[0]._replace(status = "waiting")
                
        creation_list[priority2_list[0].PID] = creation_list[priority2_list[0].PID]._replace(status = "running")
        current_running = priority2_list[0].PID

    elif len(priority2_list) == 0 and len(priority1_list) != 0:
        if current_running != "init" and current_running in creation_list:
            creation_list[current_running] = creation_list[current_running]._replace(status = "waiting")
        priority1_list[0] = priority1_list[0]._replace(status = "running")
        creation_list[priority1_list[0].PID] = creation_list[priority1_list[0].PID]._replace(status = "running")
        current_running = priority1_list[0].PID

    elif len(priority2_list) == 0 and len(priority1_list) == 0:
        current_running = "init"

    ##print("\nThe current running process is : ", current_running)
    to_write.append(current_running)




def resource_management_request(resource, request):
    ##check if resource is available
    ##calculate overall request made; so need to loop to see if that process has already wait/or hold that resource; verify that total > available
    ## if enough is available, grant access and update resource holding and resource_available_waiting
    flag = 0
    
    if current_running in resource_holding:
        for i in resource_holding[current_running]:
            if i.p_name == resource:
                if (i.amount + request) > int(resource[-1]):
                    ##print("This process is currently holding some resource, with this request, the amount exceed resource available: ERROR\n")
                    to_write.append("error")
                    flag = 1
                    return flag
    ##there is enough to grant
    if resource_available_waiting[resource].aval >= request:
        if current_running not in resource_holding:
            resource_holding[current_running] = [resource_hold(resource, request)]
        
        
        elif current_running in resource_holding:
            mark = 0
            temp_list = resource_holding[current_running]
            for e in range(len(resource_holding[current_running])):
                if resource_holding[current_running][e].p_name == resource:
                    old_amt = resource_holding[current_running][e].amount
                    temp_list[e] = resource_hold(resource, old_amt + i.amount)
                    resource_holding[current_running] = temp_list
                    mark = 1
                    break
                if mark == 0:
                    resource_holding[current_running].append(resource_hold(resource, request))
        amt = resource_available_waiting[resource].aval
        ##resource_holding[current_running].append( resource_hold(resource, request))
        resource_available_waiting[resource] = resource_available_waiting[resource]._replace(aval = amt - request)
        return 0
    ##when there is not enough resource available put it in the resource_available_waitlist; remove it from the current priority list
    ##find the next available one-> probably need to call the scheduler again to find the next available one
    ##
    ##release method: first go to resource holding-> release resource; which is gonna be updated in the resource_available_waiting; once the available
    ##list is updated, loop through the waiting list and find out which resource can be granted; if granted, put it back into the correct priority_list
    ##also,update in the resource_holding list,
    ##***question: when release a resource and found a process that can be run in the waiting list: add back to priority list or make it run right away?
    ##also need to make sure that when delete a process, that process need to release resources, and it's childrent too, then found out
    ##the next available target

    if resource_available_waiting[resource].aval < request:
        temp_list = resource_available_waiting[resource].waiting
        resource_available_waiting[resource] = resource_available_waiting[resource]._replace(waiting = temp_list + [resource_wait(current_running, request)])
        
        ##remove from priority; make a remove function?
        num = creation_list[current_running].priority
        
        if int(num) == 1:
            for i in range(len(priority1_list)):
                if priority1_list[i].PID == current_running:
                    priority1_list.pop(i)
                    break
        elif int(num) == 2:
            for i in range(len(priority2_list)):
                if priority2_list[i].PID == current_running:
                    priority2_list.pop(i)
                    break


def find_waiting_process_on_release(resource):
    ##loop through list-> of resource# waiting list:
    ##see if the current available can satisfied any waiting process
    ##if so remove it from the list and add it back to the correct priority list
    
    available = resource_available_waiting[resource].aval
    remove_obj = []
    temp_list = resource_available_waiting[resource].waiting
    
    for i in resource_available_waiting[resource].waiting:
        if available >= i.amount:
            available = available - i.amount
            remove_obj.append(i)
            info = creation_list[i.r_name]
            priority = info.priority
            if int(priority) == 1:
                priority1_list.append(info)
            elif int(priority) ==2:
                priority2_list.append(info)

            if i.r_name not in resource_holding:
                resource_holding[i.r_name] = [resource_hold(resource, i.amount)]
                
            elif i.r_name in resource_holding:
                mark = 0
                temp_list1 = resource_holding[i.r_name]
                for e in range(len(resource_holding[i.r_name])):
                    if resource_holding[i.r_name][e].p_name == resource:
                        old_amt = resource_holding[i.r_name][e].amount
                        temp_list1[e] = resource_hold(resource, old_amt + i.amount)
                        resource_holding[i.r_name] = temp_list1
                        mark = 1
                        break
                if mark == 0:
                    resource_holding[i.r_name].append(resource_hold(resource, i.amount))
        else:
            break
            
    resource_available_waiting[resource] = resource_available_waiting[resource]._replace(aval = available)
    for i in remove_obj:
        temp_list.remove(i)
    resource_available_waiting[resource] = resource_available_waiting[resource]._replace(waiting = temp_list)
    
             
def resource_management_release(resource, request):

    flag=0
    if current_running not in resource_holding:
        ##print("This process does not hold any resources: ERROR\n")
        to_write.append("error")
        flag = 1
        return flag
    
    if current_running in resource_holding:
        found = 0
        for i in resource_holding[current_running]:
            if i.p_name == resource:
                if i.amount < request:
                    ##print("This process does not hold that many resources: ERROR\n")
                    to_write.append("error")
                    flag = 1
                    return flag
                else:
                    found = 1
                    break
        if found == 0:
            ##print("This process does not hold this resource: ERRor\n")
            to_write.append("error")
            flag =1
            return flag
            

    temp = resource_holding[current_running]
    new_amt = 0
    index = 0
    for i in range(len(resource_holding[current_running])):
        if resource_holding[current_running][i].p_name == resource:
            if resource_holding[current_running][i].amount > request:
                new_amt = resource_holding[current_running][i].amount - request
                index = i
                break
    temp_aval = resource_available_waiting[resource].aval
    if new_amt == 0:
        temp.pop(index)
        resource_available_waiting[resource] = resource_available_waiting[resource]._replace(aval = temp_aval + request)
    elif new_amt > 0:
        temp[index] = resource_hold(resource, new_amt)
        resource_holding[current_running] = temp
        resource_available_waiting[resource] = resource_available_waiting[resource]._replace(aval = temp_aval + request)

    find_waiting_process_on_release(resource)


def descendent_check(c_list, target):
    if len(creation_list[target].child) == 0:
        return
    for i in creation_list[target].child:
        c_list.append(i)
        descendent_check(c_list, i)
        
    
def find_index_to_remove(target):
    target_PCB = creation_list[target]
    del creation_list[target]
    
    if target_PCB.priority == "2":
        for i in range(len(priority2_list)):
            if priority2_list[i].PID == target:
                priority2_list.pop(i)
##                if target_PCB.parent != "init" and target_PCB.parent in creation_list:
##                    temp_child = creation_list[target_PCB.parent].child
##                    temp_child.remove(target)
                    ##creation_list[target_PCB.parent] = creation_list[target_PCB.parent]._replace(child = temp_child)     
                break
       
    elif target_PCB.priority == "1":
        for i in range(len(priority1_list)):
            if priority1_list[i].PID == target:
                priority1_list.pop(i)
##                if target_PCB.parent != "init" and target_PCB.parent in creation_list:
##                    temp_child = creation_list[target_PCB.parent].child
##                    temp_child.remove(target)
                    ##creation_list[target_PCB.parent] = creation_list[target_PCB.parent]._replace(child = temp_child)
                break
      
    if target_PCB.parent != "init" and target_PCB.parent in creation_list:
        tempo_child = creation_list[target_PCB.parent].child
        tempo_child.remove(target)
        creation_list[target_PCB.parent] = creation_list[target_PCB.parent]._replace(child = tempo_child)   
    
    ##release resource-> remove that from resource holding; update in available waiting;call the find available waiting;
    ##but need to delete its existence in every waiting list first

    ##removing the process from waiting for any other resources
    for x,y in resource_available_waiting.items():
        holding_temp = []
        temp_list = y.waiting
        for i in y.waiting:
            if i.r_name == target:
                holding_temp.append(i)
                value = i.amount
                break
        for e in holding_temp:
            temp_list.remove(e)
        resource_available_waiting[x] = RCB(y.aval,temp_list)

    ##restoring the holding resources
    if target in resource_holding:
        temp = resource_holding[target]
        for i in resource_holding[target]:
            prev_value = resource_available_waiting[i.p_name].aval
            resource_available_waiting[i.p_name] = resource_available_waiting[i.p_name]._replace(aval = i.amount + prev_value)
            find_waiting_process_on_release(i.p_name)
        del resource_holding[target]
                
    if (len(target_PCB.child) > 0):
        for i in target_PCB.child:
            find_index_to_remove(i)


def parsing_input(line):
    global current_running
    new_line = line.split()
    ##print("-" * 100)
    ##print("\nThis is the input: ", new_line)

    if len(new_line) == 0:
        to_write.append("\n")
        return

    if new_line[0] == "init":
        creation_list.clear()
        priority2_list.clear()
        priority1_list.clear()
        resource_holding.clear()
        resource_available_waiting.clear()
        set_up()
        temp = current_running
        current_running = "init"

        if temp == "init" and new_line[0] == "init":
            to_write.append("init")
            return
        
        
    elif new_line[0] == "cr":
        if new_line[1] in creation_list:
            ##print("This process already exists: ERROR\n")
            to_write.append("error")
            return

        if new_line[2] not in ["1","2"]:
            #print("ERROR\n")
            to_write.append("error")
            return
        
        creation_list[new_line[1]] = PCB(PID = new_line[1], status = "waiting", resource = [],parent = current_running, child = [], priority = new_line[2])
        if current_running != "init":
            temp = creation_list[current_running].child
            creation_list[current_running] = creation_list[current_running]._replace(child = temp+ [new_line[1]])
        if new_line[2] == "1":
            priority1_list.append(PCB(PID = new_line[1], status = "waiting", resource = [],parent = current_running, child = [], priority = new_line[2]))
        if new_line[2] == "2":
            priority2_list.append(PCB(PID = new_line[1], status = "waiting", resource = [], parent= current_running, child = [], priority= new_line[2]))

    elif new_line[0] == "to":
        if current_running == "init":
            to_write.append("init")
            return
        
        if len(priority2_list) == 1:
            pass
        elif len(priority2_list) > 1:
            priority2_list[0] = priority2_list[0]._replace(status = "waiting")
            creation_list[priority2_list[0].PID] = creation_list[priority2_list[0].PID]._replace(status = "waiting")
            temp = priority2_list.pop(0)
            priority2_list.append(temp)
            
        elif len(priority2_list) == 0 and len(priority1_list) == 1:
            pass
        elif len(priority2_list) == 0 and len(priority1_list) > 1:
            priority1_list[0] = priority1_list[0]._replace(status = "waiting")
            creation_list[priority1_list[0].PID] = creation_list[priority1_list[0].PID]._replace(status = "waiting")
            temp = priority1_list.pop(0)
            priority1_list.append(temp)

    elif new_line[0] == "de":

        if new_line[1] == "init":
            ##print("Cannot delete init: ERROR\n")
            to_write.append("error")
            return
        if new_line[1] not in creation_list:
            ##print("This proces does not exists: ERROR\n")
            to_write.append("error")
            return
        if current_running != new_line[1] and current_running!= "init": ##check for descendent
            c_list = []
            descendent_check(c_list, current_running)
            ##print(c_list)
            if new_line[1] not in c_list:
                ##print("THIS is not a descendent of the current running: ERROR")
                to_write.append("error")
                return
        to_be_deleted = creation_list[new_line[1]]
        find_index_to_remove(to_be_deleted.PID)

    elif new_line[0] == "req":
        ##check for correct amt
        if current_running == "init":
            to_write.append("error")
            return
        
        if resource_check(new_line[1], int(new_line[2])) == 1:
            to_write.append("error")
            return
        
        if resource_management_request(new_line[1], int(new_line[2])) == 1:
            return


    elif new_line[0] == "rel":
        if current_running == "init":
            to_write.append("error")
            return
        if resource_check(new_line[1], int(new_line[2])) == 1:
            to_write.append("error")
            return
        
        if resource_management_release(new_line[1], int(new_line[2])) == 1:
            return
    
                       
    scheduler()
    ##print_creation_tree()
    ##print_priority()
    ##print_resource()




    
def reading_input(file_name):
    file = open(file_name)
    scheduler()
    for item in file:
        try:
            parsing_input(item)
        except:
            to_write.append("error")

    file.close()


def write_to_file():
    file = open("E://72114439.txt", 'w')
    for i in to_write:
        if i == "\n":
            file.write(i)
        else:
            file.write(i+' ')
    file.close()

        
def main():
    
    set_up()
    reading_input("E://input.txt")
    write_to_file()
       
main()
