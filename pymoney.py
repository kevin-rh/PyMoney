import sys

print_Desc="Description"
print_Amount="Amount"
cmd_set = {'add','view','delete','exit'}

money = 0
list_record = []

def input_money():
    money=0
    while(True):
        try:
            money= int(input("How much money do you have?"))
        except ValueError:
            print("Invalid value for money. Set to 0 by default.\n")
        else:
            return money


# Main

# Read File Handling
try:
    fh=open('records.txt',mode='r')
except FileNotFoundError:   # File did not exist
    money = input_money()
else:
    try:
        money = int(fh.readline())
    except ValueError:      # File is empty
        money = input_money()
    else:                   # Read data
        list_record = [ tuple(data.split(', ')) for data in fh.readlines()]
    finally:                # Always close the file
        fh.close()


# Input Command
while(True):
    try:
        cmd = input("What do you want to do (add / view / delete / exit)? ")
        assert cmd in cmd_set
    except AssertionError:
        print("Invalid command.\nAvailable command:",end='')
        print(cmd_set)
        continue

    if cmd == "add":
        #try:
        new_record = input("Add an expense or income record with description and an amount:\n")
        new_list_record = [(tuple([data.split()[0], int(data.split()[1])])) for data in new_record.split(',')]
        #except:
        #print("Invalid format. Should be <description> <amount> example: breakfast -50")
        #else:
        list_record += new_list_record
        for data in new_list_record:
            money += data[1]

    elif cmd == "view":
        print("Here\'s your expense and income records:")
        print(f"{print_Desc:<25s} {print_Amount:^8s}")
        print("="*25+" "+"="*8)
        for data in list_record:
            print(f'{data[0]:<25s} {data[1]:>8d}')

        print("="*25+" "+"="*8)
        print("Now you have %d dollars.\n" %money)

    elif cmd == "delete":
        while(True):
            try:
                del_desc,del_amount = input("Which record do you want to delete? ").split()
                del_data = tuple([del_desc, int(del_amount)])
            except:
                print("Input format should be <description> <amount>")
            else:
                break

        print("\nHere's data found inside in your records:\n")
        print(f"Index\t{print_Desc:<25s} {print_Amount:^8s}")
        print("="*5+"\t"+"="*25+" "+"="*8)

        data_idx_found = []

        for i,data in enumerate(list_record):
            if data == del_data:
                id_i = i+1
                print(f"{(id_i):>5d}\t{data[0]:<25s} {data[1]:>8d}")
                data_idx_found.append(i)
        print("="*5+"\t"+"="*25+" "+"="*8)

        if(len(data_idx_found)==0):                 # No data was found
            print(f"Data {del_data[0]:s} {del_data[1]:d} not found.")
        elif len(data_idx_found)==1:                # Found single, do deletion immediately
            del(list_record[data_idx_found[0]])
            print("Data id:{data_idx_found[0]} deleted.\n")
            money -= del_data[1]
        else:                                       # Found multiple, do selection, do deletion
            idx = input("Which data index you want to delete? Type \"all\" for all. ")
            if(idx=='all') :
                for m,i in enumerate(data_idx_found):
                    print("Data id:{i} deleted.")
                    del(list_record[i-m])
                    print("\n")
                    money -= del_data[1]*(len(data_idx_found))
            else :
                try:
                    del(list_record[int(idx)-1])
                except:
                    print("Invalid Input")
                else:
                    print("Data id:{idx} deleted\n")
                    money -= del_data[1]
    elif cmd == "exit":
        break

# Write File
record_pair_list = [', '.join(i) for i in list_record]
record_line_list = '\n'.join(record_pair_list)

fh = open('records.txt',mode='w')
fh.write(f'{money}\n')              # write money at first line
fh.writelines(record_line_list)     # write record list
fh.close()
