temp = [1,2,3,6,8,9]
def binarysearch(l, r, target):
    while l < r:
        m = ((l + r) // 2)
        print(temp[m], m, l, r)
        if target < temp[m]:
            r = m
        else:
            l = m + 1
    if target >= temp[m]:
        temp.insert(m+1,target)
    else:
        temp.insert(m,target)       
    #course_lines.insert(m, target)
print(temp)
binarysearch(0,len(temp),10)
print(temp)
binarysearch(0,len(temp),1.5)
print(temp)
binarysearch(0,len(temp),7)
print(temp)