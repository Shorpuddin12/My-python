intervals = [[1,3],[2,6],[8,10],[15,18]]

intervals.sort()
merged = [intervals[0]]

for s, e in intervals[1:]:
    if s <= merged[-1][1]:
        merged[-1][1] = max(e, merged[-1][1])
    else:
        merged.append([s, e])

print(merged)



