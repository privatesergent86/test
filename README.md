
students = []  # empty list to store people

while True:
    person = {
        "id_number": input("Enter id_number: "),
        "name": input("Enter name: "),
        "age": int(input("Enter age: "))
    }

    students.append(person)  # add the dictionary to the list

    more = input("Do you want to add another person? (y/n): ")
    if more.lower() != "y":
        break

print("All Students registered:")
for S in students:
    print(f"- {S['id_number']} {S['name']}, age: {S['age']}")
