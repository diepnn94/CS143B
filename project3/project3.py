from collections import namedtuple
bitmap_entry = namedtuple('bitmap_entry', 'status reserved_by info')
info = namedtuple('info', 'segment page offset start end')
TLB_entry = namedtuple('TLB_entry', 'rank sp f')
bitmap = []
PA = []
log = []
to_return = []
to_return2= []
TLB = []

def setup_TLB():
    for i in range(4):
        TLB.append(TLB_entry(i,(0,0),0))
        
def setup_PA():
    for i in range(524800):
        PA.append(0)


def setup_bitmap():
    for i in range(1025):
        bitmap.append(bitmap_entry(0,0,(0,0)))
    bitmap[0] = bitmap[0]._replace(status = 1)

def update_TLB(segment, page, address):
    for i in range(len(TLB)):
        if int(TLB[i].rank) == 0:
            TLB[i] = TLB[i]._replace(sp = (segment, page))
            TLB[i] = TLB[i]._replace(f = address)
            for e in range(len(TLB)):
                TLB[e] = TLB[e]._replace(rank = int(TLB[e].rank)-1)
            TLB[i] = TLB[i]._replace(rank = 3)
            return


def allocate_page_table(segment):
    for i in range(1, len(bitmap)-1):
        if int(bitmap[i].status == 0) and int(bitmap[(i+1)].status) ==0:
            bitmap[i] = bitmap[i]._replace(status = 1)
            bitmap[i+1] = bitmap[i+1]._replace(status = 1)
            bitmap[i] = bitmap[i]._replace(reserved_by = segment)
            bitmap[i+1] = bitmap[i+1]._replace(reserved_by = segment)
            bitmap[i] = bitmap[i]._replace(info = (i*512, (i*512)+1024))
            bitmap[i+1] = bitmap[i+1]._replace(info = (i*512, (i*512)+1024))
            log.append(info(segment, bitmap[i].info[0], "NA", bitmap[i].info[0], bitmap[i].info[1]))
            
            return bitmap[i]

def allocate_page(page_address):
    for i in range(1, len(bitmap)):
        if int(bitmap[i].status == 0):
            bitmap[i] = bitmap[i]._replace(status = 1)
            bitmap[i] = bitmap[i]._replace(reserved_by = page_address)
            bitmap[i] = bitmap[i]._replace(info = (i*512, (i*512)+512))
            log.append(info(page_address, bitmap[i].info[0], "NA", bitmap[i].info[0], bitmap[i].info[1]))
            return bitmap[i]

def init_segment_table(segment:int, address:int):
    PA[segment]= address
    bitmap[address//512] = bitmap[address//512]._replace(status = 1)
    bitmap[(address//512)+1] = bitmap[(address//512)+1]._replace(status = 1)
    bitmap[address//512] = bitmap[address//512]._replace(reserved_by = segment)
    bitmap[(address//512)+1] = bitmap[(address//512)+1]._replace(reserved_by = segment)
    bitmap[address//512] = bitmap[address//512]._replace(info = (address, address+1024))
    bitmap[(address//512)+1] = bitmap[(address//512)+1]._replace(info = (address, address+1024))

    log.append(info(segment, address, "NA", address, address+1024))


def init_page_table(segment:int, page_offset: int, address: int):
    PA[PA[segment] + page_offset] = address
##    update_TLB(segment, page_offset, address)
    if address != -1:
        bitmap[address//512] = bitmap[address//512]._replace(status = 1)
        bitmap[address//512] = bitmap[address//512]._replace(reserved_by = (segment, page_offset))
        bitmap[address//512] = bitmap[address//512]._replace(info = (address, address+512))
        log.append(info(segment, page_offset,"NA" , address, address+512))
        
    else:
        log.append(info(segment, page_offset, "NA", -1, -1))

def log_output():
    for i in log:
        print("segment {} page {} offset {} start {} end {}".format(i.segment, i.page, i.offset, i.start, i.end))
    

def to_bin(num, base):

    x = bin(num)
    y = x[2:].zfill(base)
    return y


def extract_spw(bin_num):
    s= bin_num[0:9]
    p = bin_num[9:19]
    w= bin_num[19:]
    return (s,p,w)



def spw_to_int(spw):
    x = int(spw[0],2)
    y = int(spw[1],2)
    z = int(spw[2],2)
    return(x,y,z)

def TLB_search(segment, address, offset):
    for i in range(len(TLB)):
        if int(TLB[i].sp[0]) == segment and int(TLB[i].sp[1]) == address:
            TLB[i] = TLB[i]._replace(sp = (segment, address))
            TLB[i] = TLB[i]._replace(f = PA[PA[segment]+address])
            if int(TLB[i].rank) == 0:
                for e in range(len(TLB)):
                    TLB[e] = TLB[e]._replace(rank = int(TLB[e].rank)-1)
            elif int(TLB[i].rank) ==1:
                for e in range(len(TLB)):
                    if int(TLB[e].rank)!= 0 and int(TLB[e].rank) != 1:
                        TLB[e] = TLB[e]._replace(rank = int(TLB[e].rank)-1)
                
            elif int(TLB[i].rank) == 2:
                for e in range(len(TLB)):
                    if int(TLB[e].rank) == 3:
                        TLB[e] = TLB[e]._replace(rank = int(TLB[e].rank)-1)
            TLB[i] = TLB[i]._replace(rank =3)
            result = int(TLB[i].f) + offset
            to_return2.append(('h',result))
            
            return 1
    return 0

def read_write_VA_PA(mode:int, VA:int):

    binary = to_bin(VA, 28)
    spw = extract_spw(binary)
    result = spw_to_int(spw)
    segment = int(result[0])
    page = int(result[1])
    offset = int(result[2])
    
    
    if mode == 0:
        
        if int(PA[segment]) == -1 or  (int(PA[PA[segment]+page]) == -1 and int(PA[segment]) != 0):
            to_return.append("pf")
            to_return2.append(("m", "pf"))
            
        elif int(PA[segment]) == 0 or int(PA[PA[segment]+page]) == 0:
            to_return.append("err")
            to_return2.append(("m", "err"))
        else:
            to_return.append(PA[PA[segment]+page]+offset)
            result = TLB_search(segment, page, offset)
            if int(result) == 0:
                update_TLB(segment, page, PA[PA[segment]+page])
                to_return2.append(("m", PA[PA[segment]+page]+offset))

    elif mode == 1:
        if int(PA[segment]) == -1 or int(PA[PA[segment]+ page]) == -1:
            to_return.append("pf")
            to_return2.append(("m", "pf"))

        elif int(PA[segment]) == 0:
            address = allocate_page_table(segment)
            PA[segment] = int(address.info[0])
            page_address = allocate_page(int(address.info[0]))
            PA[PA[segment]+ page] = page_address.info[0]
            update_TLB(segment, page, page_address.info[0])
            to_return.append(page_address.info[0]+offset)
            to_return2.append(("m", page_address.info[0] + offset))
            
        elif int(PA[PA[segment] + page]) == 0:
            page_addr = allocate_page(int(PA[PA[segment] + page]))
            PA[PA[segment]+ page] = page_addr.info[0]
            update_TLB(segment, page, page_addr.info[0])
            to_return.append(page_addr.info[0]+offset)
            to_return2.append(("m", page_addr.info[0] + offset))
            
        else:
            to_return.append(PA[PA[segment]+page] + offset)
            result = TLB_search(segment, page, offset)
            
            if int(result) == 0:
                update_TLB(segment, page, PA[PA[segment]+page])
                to_return2.append(("m", PA[PA[segment]+page]+offset))

def reading_input1():
    file = open('E:\\input1.txt')
    line1 = file.readline()
    line2 = file.readline()
    line1 = line1.split()
    line2 = line2.split()

    step = 2
    
    for i in range(0, len(line1), step):
        
        init_segment_table(int(line1[i]), int(line1[i+1]))
       

    step = 3
    for i in range(0, len(line2), step):
       
        init_page_table(int(line2[i+1]), int(line2[i]), int(line2[i+2]))

    file.close()
    
def reading_input2():
    file = open('E:\\input2.txt')
    line = file.readline().split()
    step = 2
    for i in range(0, len(line), step):
        read_write_VA_PA(int(line[i]), int(line[i+1]))

    file.close()
def write_output():
    file = open("E:\\72114439-notlb.txt", 'w')
    file2 = open("E:\\72114439-tlb.txt", 'w')
    for i in to_return:
        file.write(str(i))
        file.write(' ')

    for i in to_return2:
        file2.write(str(i[0]))
        file2.write(' ')
        file2.write(str(i[1]))
        file2.write(' ')
    file.close()
    file2.close()
    
def main():
    setup_PA()
    setup_TLB()
    setup_bitmap()
    reading_input1()
    reading_input2()
    print('\n')
    print(to_return)
    print('\nTLB\n')
    print(to_return2)
    print("\n")
    write_output()

    
main()





