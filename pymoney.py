# Headers
import sys
print_Category = "Category"
print_Desc = "Description"
print_Amount = "Amount"
cmd_set = (
    "add", 
    "view", 
    "delete", 
    "view categories", 
    "find", 
    "exit",
)

# Program Functions
def input_money():
    """Insert the amount money at the initialization."""
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
    """Initialize this program at start.
    Read data in file if available, else request initialize new data.
    """
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
                record = [tuple([data.split(', ')[1], int(data.split(', ')[2]), data.split(', ')[0]]) for data in fh.readlines()]
                # record_pair_list = [(catg+', '+name+', '+str(amt)) for name,amt,catg in record]
    except FileNotFoundError:       # Exception: File did not exist
        money = input_money()
    return money, record

def add(money, record, categories):
    """Add new record.

    Keyword arguments:
    money       -- the total money
    record      -- the entire record list
    categories  -- the entire category list
    """
    while(True):
        try:
            new_record = input("Add an expense or income record with description and an amount:\n")
            assert new_record != 'q'
            new_record = new_record.split()
            [category, desc, amount] = new_record
            if not is_category_valid(categories, category):
                categories = add_categories(categories, category)
        except AssertionError:
            print("Cancel Add Fucntion\n")
            return money, record, categories
        except ValueError: # Exception if can not split into two (desc, amount)
            print("Invalid format.\nFormat: <category> <description> <amount>. e.g.: food breakfast -50\n")
        else:
            try:
                amount_int = int(amount)
            except ValueError:
                print("Invalid format. <amount> should be an integer.\n")
            else:
                record.append(tuple([desc, amount_int, category]))
                money += amount_int
                print()
                return money, record, categories

def view(money, record, categories): #TODO: Check the categories part
    """View record.

    Keyword arguments:
    money       -- the total money
    record      -- the entire record list
    categories  -- the entire category list
    """
    print(f"Here\'s your expense and income records:")
    print(f"{print_Category:<25s} {print_Desc:<25s} {print_Amount:^8s}")
    print("="*25 +" "+ "="*25 + " "+"="*8)
    for data in record:
        print(f'{data[2]:<25s} {data[0]:<25s} {data[1]:>8d}')
    print("="*25 +" "+ "="*25 + " "+"="*8)
    print("Now you have %d dollars.\n" %money)
    pass

def delete(money, record, categories): #TODO: Bind with categories
    """Delete record.

    Keyword arguments:
    money       -- the total money
    record      -- the entire record list
    categories  -- the entire category list
    """
    while(True):
        try:
            delete = input("Which record do you want to delete? ").split()
            assert delete != 'q'
        except AssertionError:
            print("Cancel Deletion Function\n")
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

def save(money, record, categories):
    """Write record inside a file.

    Keyword arguments:
    money       -- the total money
    record      -- the entire record list
    categories  -- the entire category list
    """
    # DEBUG
    #print(record)
    record_pair_list = [(catg+', '+name+', '+str(amt)) for name,amt,catg in record]
    record_line_list = '\n'.join(record_pair_list)
    
    # Write the data
    try:
        with open("records.txt","w") as fh:
            try:
                fh.write(f'{money}\n')              # write money at first line
                fh.writelines(record_line_list)     # write record list
                fh.close()
            except:      # Exception: File first line not an Integer
                print("Fail to write the recorded file.\n")
            else:                   # Read data to the record variable
                print("File sucessfully saved.\n")
    except FileNotFoundError:       # Exception: File did not exist
        print("File did not existed. Failed to write data to the file!\n")
    
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
    """Input command error control.
    Control when a command in the intreperter is correct or not.
    """
    while(True):
        try:
            cmd = input("What do you want to do ("+" / ".join(cmd_set) +")? ")
            assert cmd in cmd_set
        except AssertionError:
            print("Invalid command.\nAvailable command: "+" / ".join(cmd_set) +".\n")
        else:
            print()
            return cmd


def find(records, categories):
    """Find record by categories.

    Keyword arguments:
    record      -- the entire record list
    categories  -- the entire category list
    """
    while(True):
        try:
            category = input("Which category do you want to find? ")
            assert category != 'q'
        except AssertionError:
            print("Cancel Find Function\n")
            break
        else:
            try:
                if category != "all": assert is_category_valid(categories, category) == True
            except AssertionError:
                print(f"Category {category:s} is not available!\n")
            except ValueError:
                print(f"Category should be a string.\n")
            else:
                #TODO: print the filtered records
                amounts = 0
                print(f"Here\'s your { category if category!='all' else 'expense and income'} records:")
                # Headers
                print(f"{print_Category:<25s} {print_Desc:<25s} {print_Amount:^8s}")
                print("="*25 +" "+ "="*25 + " "+"="*8)
                
                for data in filter(lambda rec: rec[2] in find_subcategories(categories, category) if category != 'all' else initialize_categories(), records):
                    print(f'{data[2]:<25s} {data[0]:<25s} {data[1]:>8d}')
                    amounts += data[1]
                print("="*25 +" "+ "="*25 + " "+"="*8)
                print(f"The total amount above is {amounts:d} dollars.\n")
                break
    pass

# Categories Function
def initialize_categories ():
    """Return initialized all category in form of a list."""
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

def find_subcategories(categories, category):
    """Return all subcategories of a category as a list.
    Return empty list [] if no category is found.

    Keyword arguments:
    categories  -- the entire category list
    category    -- the searched category
    """
    if type(categories) == list:
        for i, v in enumerate(categories):
            p = find_subcategories(v, category)
            if p == True:
                return flatten(categories[i:i+2 if (i+2) <= len(categories) else i+1])
            if p != []:
                return p
    return categories == category or []

def is_category_valid(categories, category):
    """Return True if a category is exist inside the category list.
    Otherwise, return False.

    Keyword arguments:
    categories  -- the entire category list
    category    -- the searched category
    """
    if type(category) in {list, tuple}: # Only has one value
        for cat in category:
            return is_category_valid(categories, cat)
    
    return False if find_subcategories(categories, category) == [] else True

def view_categories(categories, depth=0):
    """Print all the whole category list.

    Keyword arguments:
    categories  -- the entire category list
    depth       -- the depth occur recursively (default = 0)
    """
    if depth == 0: print("Category: ")
    for i, atom in enumerate(categories):
        if type(atom) not in {list, tuple}:
            print(' '*4*depth + '- ' + atom)
        else :
            view_categories(atom, depth+1)
        # depth+'.'+str(i+1) if depth else str(i+1)   
    if depth ==0: print()
      
def flatten(L):
    """Return a flat list that contains all element in the nested list L.
    
    For example, flatten([1, 2, [3, [4], 5]]) returns [1, 2, 3, 4, 5].
    
    Keyword arguments:
    L   -- recursive structured list
    """
    if type(L) not in {list, tuple}:
        return [L]
    flat = []
    for atom in L:
        flat.extend(flatten(atom))
    return flat

# Main Program
money, list_record = initialize()
categories = initialize_categories()
# Input Command
while True:
    cmd = input_command()
    if cmd == "add":
        money, list_record, categories = add(money, list_record, categories)
    elif cmd == "view":
       view(money, list_record, categories)
    elif cmd == "delete":
        money, list_record, categories = delete(money, list_record, categories)
    elif cmd == "view categories":
        view_categories(categories)
    elif cmd == "find":
        find(list_record, categories)
    elif cmd == "exit":
        if save(money, list_record, categories):
            break
        else :
            print("Something went wrong, while writing the data to the file.")
print("See you, thank you!")
