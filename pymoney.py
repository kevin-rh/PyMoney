money = input("How much money do you have? ")

record = input("Add an expense or income record with description and an amount:\n")
name,price = record.split()

total = int(money) + int(price)

print("Now you have %d dollars." %total)
