s = "abcabcbb"

res = ""       # এখানে আমরা current substring রাখব
longest = ""   # এখানে সবচেয়ে বড় substring রাখব

for c in s:
    if c in res:
        # যদি character আগে থাকে → পুরোনো অংশ কেটে দাও
        res = res[res.index(c)+1:]
    res += c   # নতুন character যোগ করো

    # যদি এখনকার substring বড় হয় → longest update করো
    if len(res) > len(longest):
        longest = res

print("Longest substring:", longest)
print("Length:", len(longest))
