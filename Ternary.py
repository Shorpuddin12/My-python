num1 = 30
num2 = 40
num3 = 20
num4 = 50 
num5 = 60 
num6 = 70
max_num = (
    num1 if (num1 > num2 and num1 > num3 and num1 > num4 and num1 > num5 and num1 > num6)
    else (num2 if (num2 > num3 and num2 > num4 and num2 > num5 and num2>num6)
    else (num3 if (num3 > num4 and num3 > num5 and num3>num6)
    else (num4 if (num4 > num5 and  num4 >num6)
    else (num5 if num5 > num6 else num6)))))
print("The largest number is ", max_num)

