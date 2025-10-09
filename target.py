#list = [2,4,3,6,4,5]
#target = 7
#output 4,3
# Two sum
nums = [2,7,8,5,6]
target = 9
for i  in nums:
    for j in nums:
        if i+j == target and i <=j:
            print(i,j)
            break
