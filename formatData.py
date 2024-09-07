from scrapeScheduleofClasses import res
from scrapeCourseCatalog import res2
import heapq
import re


def split_key(s):
    # Split using a regular expression that separates numeric and alpha components
    return [int(x) if x.isdigit() else x for x in re.split('([0-9]+)', s) if x]


cache = set()
all = []

for i in res:
    index = 0
    while i[index] != "'" or i[index-1] != ",":
        index += 1
    index2 = index+1
    while i[index2] != "'":
        index2 += 1
    #print(i)
    #print(i[index+1:index2], index+1, index2)
    cache.add(i[index+1:index2])
    heapq.heappush(all, (split_key(i[index+1:index2]),i))

for i in res2:
    index = 0
    while i[index] != "'" or i[index-1] != ",":
        index += 1
    index2 = index+1
    while i[index2] != "'":
        index2 += 1
    if i[index+1:index2] not in cache:
        heapq.heappush(all, (split_key(i[index+1:index2]),i))
        #print(i)

for i in range(len(all)):
    temp = heapq.heappop(all)
    print(temp)