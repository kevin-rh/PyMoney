money = int(input("How much money do you have? "))
record = input("Add an expense or income record with description and an amount:\n")

list_record = [(tuple([data.split()[0], int(data.split()[1])])) for data in record.split(',')]
#print (list_record)

print('Here\'s your expense and income records:')
for data in list_record:
  print(f'{data[0]:s} {data[1]:d}')
  money += data[1]

print("Now you have %d dollars." %money)
