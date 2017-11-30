from collections import namedtuple
from copy import deepcopy

process = namedtuple('process', 'arrival burst remain turn_around PID level level_count to_print')
level = [1,2,4,8,16, 32, 64, 128, 256]
to_return = []


def output(result):
    try:
        ave = str(sum(int(i.turn_around) for i in result)/len(result))
        sep = ave.find('.')
        if (len(ave) - sep -1 < 2):
            ave = ave + "0"
        ave = ave[0:sep+3]
    except:
        ave = str(sum(int(i.turn_around) for i in result)/len(result))
    to_return.append(ave)
    to_return.append(' ')
    for i in result:
        ##print("Process" , i.PID, "turnaround time", i.turn_around)
        to_return.append(round(int(i.turn_around),2))
        to_return.append(' ')
    to_return.append("\n")
    ##print("\nAverage", sum(int(i.turn_around) for i in result)/len(result))
        
    
    


def FIFO(result):
    
    start = deepcopy(result)
    start.sort(key = lambda x: [int(x.arrival), int(x.PID)], reverse = False)
    
    finished = []
                  
    time = 0

    while True:

        if int(start[0].remain) == 0:
            start[0] = start[0]._replace(turn_around = time - int(start[0].arrival))
            finished.append(start[0])
            start.remove(start[0])

        if (len(start) == 0):
            break
        if (int(start[0].arrival) > time):
            pass
        elif int(start[0].remain) > 0:
            start[0] = start[0]._replace(remain = int(start[0].remain)-1)
        time = time+1
    
    return finished


def SJF_sort(result, time):
    to_return = []
    not_yet_arrived = []
    for i in result:
        if int(i.arrival) <= time:
            to_return.append(i)
        else:
            not_yet_arrived.append(i)

    to_return.sort(key = lambda x: [int(x.burst), int(x.PID)], reverse = False)
    to_return = to_return + not_yet_arrived
    return to_return


def SJF(result):
    
    start= deepcopy(result)
    start.sort(key = lambda x: [int(x.arrival), int(x.burst), int(x.PID)], reverse = False)
    

    finished = []
    time = 0

    while True:
        if int(start[0].remain) == 0:
            start[0] = start[0]._replace(turn_around = time - int(start[0].arrival))
            finished.append(start[0])
            start.remove(start[0])
            start = SJF_sort(start, time)

        if (len(start) == 0):
            break
        if (int(start[0].arrival) > time):
            pass
        elif int(start[0].remain) > 0:
            start[0] = start[0]._replace(remain = int(start[0].remain)-1)
        time = time+1
        
    return finished


def SRT_sort(result, time):
    to_return = []
    not_yet_arrived = []
    for i in result:
        if int(i.arrival) <= time:
            to_return.append(i)
        else:
            not_yet_arrived.append(i)

    to_return.sort(key = lambda x: [int(x.remain), int(x.PID)], reverse = False)
    to_return = to_return + not_yet_arrived
    return to_return

def SRT(result):
    ##print("SRT");
    start = deepcopy(result);
    start.sort(key=lambda x: [int(x.arrival), int(x.remain), int(x.PID)], reverse = False);
    finished = []
    time = 0

    while (True):
        if (len(start) == 0):
            break
        if (int(start[0].arrival) > time):
            pass
        elif (int(start[0].remain) > 0):
            start[0] = start[0]._replace(remain = int(start[0].remain)-1)
            if (int(start[0].remain) == 0):
                start[0] = start[0]._replace(turn_around = time - int(start[0].arrival) +1 )
                finished.append(start[0])
                start.remove(start[0])
                
        time = time +1
        start = SRT_sort(start, time)
    
    return finished


def MLF_sort(result, time):
    temp = []
    not_yet_arrived = []
    block = []
    to_return = []
    for i in result:
        if int(i.arrival) <= time:
            temp.append(i)
        else:
            not_yet_arrived.append(i)
    temp.sort(key = lambda x: [int(x.level), int(x.PID)], reverse = False)
    for i in temp:
        if int(i.level_count) < level[int(i.level)-1] or int(i.remain) == 0:
            to_return.append(i)
        else:
            i = i._replace(level = int(i.level)+1)
            i = i._replace(level_count = 0)
            block.append(i)
    if (len(to_return) == 0):
        block.sort(key = lambda x: [int(x.level),int(x.PID)], reverse = False)
        
    to_return.sort(key = lambda x: [int(x.level), int(x.PID)], reverse = False)
    ##print("TO_RETURN", to_return)
    ##print("BLOCK", block)
    to_return = to_return+block
    to_return.sort(key = lambda x: [int(x.level), int(x.PID)], reverse = False)
    ##to_return = to_return + block + not_yet_arrived
    
    return to_return+not_yet_arrived

def MLF(result):
    ##print("MLF");
    start = deepcopy(result);
    start.sort(key=lambda x: [int(x.arrival), int(x.level), int(x.PID)], reverse = False);
    finished = []
    time = 0

    while (True):


        start = MLF_sort(start, time)
        ##print(time, "and ", start[0].PID, " and ", start[0].level, " and ", start[0].level_count)
        
        if (int(start[0].arrival) > time):
            pass
        
        elif (int(start[0].remain) > 0):
            start[0] = start[0]._replace(remain = int(start[0].remain)-1)
            start[0] = start[0]._replace(level_count = int(start[0].level_count) +1)

        if (int(start[0].remain) == 0):
##                print("process ", start[0].PID, " finished at time ", time)
                start[0] = start[0]._replace(turn_around = time - int(start[0].arrival)+1)
                finished.append(start[0])
                start.remove(start[0])
        if len(start) == 0:
            break
        
        
        time = time +1
        
        
        
    return finished



def computing(result):
    x = FIFO(result)
    x.sort(key = lambda x: x.to_print, reverse = False)
    output(x)
    x = SJF(result)
    x.sort(key = lambda x: x.to_print, reverse = False)
    output(x)
    x = SRT(result)
    x.sort(key = lambda x: x.to_print, reverse = False)
    output(x)
    x = MLF(result)
    x.sort(key = lambda x: x.to_print, reverse = False)
    output(x)
    ##to_return.append("\n")

def converting_to_process(line):
    process_list = []
    step = 2
    input_list = line.split()
    in_pair_list = []
    ##in_pair_list = [input_list[e:e+step] for e in range(0, len(input_list), step)]
    count = 1
    for e in range(0, len(input_list), step):
        in_pair_list.append((input_list[e:e+step], count))
        count+=1
    temp = []
    in_pair_list.sort(key = lambda x: int(x[0][0]), reverse = False)
##    print(in_pair_list)
    num = 1
    for i in in_pair_list:
        process_list.append(process(i[0][0], i[0][1], i[0][1], "NA", num, 1, 0, i[1]))
        num = num+1
    return process_list
    

    
def read_input():
    file = open("E:\\input.txt")
    for i in file:
        if (i == "\n"):
            pass
        else:
            result = converting_to_process(i)
            computing(result)
    file.close()

def write_output():
    file = open("E:\\72114439.txt", 'w')
    for i in to_return:
        file.write(str(i))
    file.close()
    
def main():
    read_input()
    write_output()

main()
