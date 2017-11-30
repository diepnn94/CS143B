
va = 1049088


def to_bin(num, base):

    x = bin(num)
    y = x[2:].zfill(base)
    return y

bin_num = to_bin(va, 28)
print(to_bin(va, 28))
print(len(bin_num))

def extract_spw(bin_num):
    s= bin_num[0:9]
    p = bin_num[9:19]
    w= bin_num[19:]
    return (s,p,w)

print(extract_spw(bin_num))

spw = extract_spw(bin_num)


def to_int(bin_num):
    x = int(bin_num, 2)
    return x

print(to_int(spw[0]))
print(to_int(spw[1]))
print(to_int(spw[2]))



