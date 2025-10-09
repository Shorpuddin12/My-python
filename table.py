from tabulate import tabulate


patients = [
    [239211, "Ibrahim", 30, "F", "Mirpur-1"],
    [239212, "Nehal", 45, "M", "Mirpur-10"],
    [239213, "Sadiya", 29, "F", "Jiya Uddan"],
    [239214, "Rhahim", 50, "M", "Dhanmondi"],
    [239215, "Eva", 35, "F", "Uttara"],
    [239216, "Frank", 40, "M", "Gulshan"]
]


headers = ["ID_Number", "Name", "Age", "Grade", "Address"]


print(tabulate(patients, headers=headers, tablefmt="psql"))
