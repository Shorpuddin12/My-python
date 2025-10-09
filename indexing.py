import  numpy as np

my_array = np.array ([1,2,3,4,5,6])

print(my_array[2])
print(my_array[2:])
print(my_array[-1])
print(my_array[-1])

new_array = np.random.randint(1,10 ,size=(3,4))
print(new_array)
print(new_array[0,1])
print(new_array[0,-1])
print("***")
array = np.random.randint(1,10,size=(2,3,3))
print(array)
print(array[0,2,1])
print(array[1,0,1])
print(array[1,2,1])


