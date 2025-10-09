def towSum (num,terget):
    new_map= {}
    for i in range (len(num)):
        nums=num[i]
        compliment= terget-nums
        if compliment in new_map:
            return [new_map[compliment],i]
        new_map[nums]=i

num = [2,7,5,6,3,4]
teget =  9

print(towSum(num,teget))


#problem 2

def reverse_array(arr):
    return arr[::-1]

# Example use:
arr = [1, 2, 3, 4, 5]
reversed_arr = reverse_array(arr)
print(reversed_arr)  # Output: [5, 4, 3, 2, 1]



