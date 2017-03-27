lis = []
with open('keep.txt', 'r') as istr:
    for i in  istr:
        lis.append(i)
with open('keep1.txt','w') as wstr:
    for i in lis:
        wstr.write(i+","),