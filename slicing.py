import numpy as np

slicing_array = np.array([1,2,3,4,5])
print(slicing_array)
print(slicing_array[1:])
print(slicing_array[0:3])
print(slicing_array[2:])

print("***")
demo_array = np.random.randint(1,10, size = (1,3,3))
print(demo_array)
print("***")
print(demo_array[0:3])