# Headers
import sys
print_Desc = "Description"
print_Amount = "Amount"
cmd_set = ("add", "view", "delete", "exit")

# Program Functions
def input_money():
    money=0
    # Loop until the money input format is correct
    print("Hi, new user!")
    while True:
        try:
            money= int(input("How much money do you have? "))
        except ValueError:  # Exception: Not an Integer
            print("Invalid value for money. Should be an Integer amount of money.\n")
        else:
            print()
            return money

def initialize():
    money = 0
    record = []
    # Read Data from a File
    try:
        with open("records.txt","r") as fh:
            try:
                line = fh.readline()
                assert line != ''
                money = int(line)
            except AssertionError:
                print("Recorded file is an empty file.\n")
                money = input_money()
            except ValueError:      # Exception: File first line not an Integer
                print("Fail to read the recorded file.\n")
                money = input_money()
            else:                   # Read data to the record variable
                print("Welcome back!\n")
                record = [ tuple([data.split(', ')[0],int(data.split(', ')[1])]) for data in fh.readlines()]
    except FileNotFoundError:       # Exception: File did not exist
        money = input_money()
    return money, record

def add(money, record):
    while(True):
        try:
            new_record = input("Add an expense or income record with description and an amount:\n")
            assert new_record != 'q'
            desc, amount = new_record.split()
        except AssertionError:
            print("Cancle Addition\n")
            return money, record
        except ValueError: # Exception if can not split into two (desc, amount)
            print("Invalid format. Expect 2 members: <description> <amount>. e.g.: breakfast -50\n")
        else:
            try:
                amount_int = int(amount)
            except ValueError:
                print("Invalid format. Amount should be an integer.\n")
            else:
                record.append(tuple([desc,amount_int]))
                money += amount_int
                print()
                return money, record

def view(money, record):
    print("Here\'s your expense and income records:")
    print(f"{print_Desc:<25s} {print_Amount:^8s}")
    print("="*25+" "+"="*8)
    for data in record:
        print(f'{data[0]:<25s} {data[1]:>8d}')

    print("="*25+" "+"="*8)
    print("Now you have %d dollars.\n" %money)
    pass

def delete(money, record):
    while(True):
        try:
            delete = input("Which record do you want to delete? ").split()
            assert delete != 'q'
        except AssertionError:
            print("Cancel Deletion\n")
            break
        else:
            try:
                assert len(delete)!=2
                del_data = tuple([delete[0], int(delete[1])]);
            except ValueError:
                print("Invalid format. Amount should be an integer.\n")
            except AssertionError:
                print("Invalid format. Expect 2 members: <description> <amount>. e.g.: breakfast -50\n")
            else:
                break

    print("\nHere's data found inside in your records:\n")
    print(f"Index\t{print_Desc:<25s} {print_Amount:^8s}")
    print("="*5+"\t"+"="*25+" "+"="*8)

    data_idx_found = []
    found = 0
    for i,data in enumerate(record):
        if data == del_data:
            found += 1
            print(f"{found:>5d}\t{data[0]:<25s} {data[1]:>8d}")
            data_idx_found.append(i)
    print("="*5+"\t"+"="*25+" "+"="*8)
    print()
    if found == 0:                 # No data was found
        print(f"Data {del_data[0]:s} {del_data[1]:d} not found.")
    elif found == 1:                # Found single, do deletion immediately
        while True:
            confirm = input("Delete the only data (y/n)? ")
            if confirm in ('y','n'):
                if confirm == 'y':
                    del(record[data_idx_found[0]])
                    print("Data id: 1 deleted.")
                    money -= del_data[1]
                break
            else :
                print("Invalid input! Must be \'y\' or \'n\'.\n")
    else:                                       # Found multiple, do selection, do deletion

        idx = input("Which data index you want to delete? Type \"all\" for all. ")
        if(idx=='all') :
            for m,i in enumerate(data_idx_found):
                ii=1+i
                print(f"Data id: {ii} deleted.")
                del(record[data_idx_found(i)-m])
            money -= (del_data[1]*(len(data_idx_found)))
        else :
            try:
                del(record[data_idx_found[int(idx)-1]])
            except ValueError:
                print(f"Invalid index input should be an integer")
            except IndexError:
                print(f"Index range from 1 to {found:d}\n")
            else:
                print(f"Data id: {idx} deleted.")
                money -= del_data[1]
    print()
    return money, record

def save(money, record):
    # DEBUG
    #print(record)
    record_pair_list = [(i+', '+str(j)) for i,j in record]
    record_line_list = '\n'.join(record_pair_list)

    fh = open('records.txt',mode='w')
    fh.write(f'{money}\n')              # write money at first line
    fh.writelines(record_line_list)     # write record list
    fh.close()
    print("File sucessfully saved.\n")
    while True:
        try:
            confirm = input("Exit (y/n)? ")
            assert confirm in ('y','n')
        except AssertionError:
            print("Invalid Input. Should be \'y\' or \'n\'.\n")
        else:
            print()
            return (confirm =='y')

def input_command():
    while(True):
        try:
            cmd = input("What do you want to do ("+" / ".join(cmd_set) +")? ")
            assert cmd in cmd_set
        except AssertionError:
            print("Invalid command.\nAvailable command: "+" / ".join(cmd_set) +".\n")
        else:
            print()
            return cmd

# Main Program
money, list_record = initialize()
# Input Command
while True:
    cmd = input_command()
    if cmd == "add":
        money, list_record = add(money, list_record)
    elif cmd == "view":
       view(money, list_record)
    elif cmd == "delete":
        money, list_record = delete(money, list_record)
    elif cmd == "exit":
        if save(money, list_record):
            break
print("See you, thank you!")
