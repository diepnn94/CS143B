

file1 = open("image1.pgm")
file2 = open("output3.pgm")

result1 = []
result2 = []
for i in file1:
    result1.append(file1.readline())

for i in file2:
    result2.append(file2.readline())

if (len(result1) == len(result2)):
    print("same SIze")


print(result1[0] == result2[0])
for i in range(len(result1)):
    if i < 3:
        print(result1[i], " ", result2[i])
    if result1[i] != result2[i]:
        print("this is the index", i)
        
print(result1[181] == result2[181])
print(result1[181])
print(result2[181])
    
##        print("THIS IS THE DIFF")
##        for x in range(len(result2[i])):
##            print(result1[i][x])
##        break
            



file1.close()
file2.close()
