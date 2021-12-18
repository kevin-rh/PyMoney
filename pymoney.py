# Headers
import sys
from typing import Type
print_Category = "Category"
print_Desc = "Description"
print_Amount = "Amount"
cmd_set = (
    "add", 
    "view", 
    "delete", 
    "view categories", 
    "add categories",
    "find", 
    "exit",
)

class Record:
    """Represent a record.
    Immutable data type.
    
    Consist of:
    _category,  -- categorize the record
    _name,      -- label the record
    _amount     -- money amount in a record
    """
    def __init__(self, category, name, amount):
        """Initialize a record."""
        if type(category) != str: raise ValueError
        if type(name) != str: raise ValueError
        self._category = category
        self._name = name
        self._amount = int(amount)

    @property
    def amount(self):
        """Return the Amount."""
        return self._amount
    @property
    def category(self):
        """Return the Category."""
        return self._category
    @property
    def name(self):
        """Return the Name."""
        return self._name

    def __eq__(self, object):
        return self._amount == object._amount\
        and self._category == object._category\
        and self._name == object._name 
    def __le__ (self, object):
        return self._category == object._category\
        and self._name == object._name 
        

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """Initialize this program at start.
        Read data in file if available, else request initialize new data.
        """
        self._money = 0
        self._record = []
        # Read Data from a File
        try:
            with open("records.txt","r") as fh:
                try:
                    line = fh.readline()
                    assert line != ''
                    self._money = int(line)
                except AssertionError:
                    print("Recorded file is an empty file.\n")
                    self.input_money()
                except ValueError:      # Exception: File first line not an Integer
                    print("Fail to read the recorded file.\n")
                    self.input_money()
                else:                   # Read data to the record variable
                    print("Welcome back!\n")
                    self._record = [Record(*data.split(', ')) for data in fh.readlines()]
                    # record_pair_list = [(catg+', '+name+', '+str(amt)) for name,amt,catg in record]
        except FileNotFoundError:       # Exception: File did not exist
            self.input_money()
        return

    def input_money(self):
        """Insert the amount money at the initialization."""
        #money=0
        # Loop until the money input format is correct
        print("Hi, new user!")
        while True:
            try:
                self._money= int(input("How much money do you have? "))
            except ValueError:  # Exception: Not an Integer
                print("Invalid value for money. Should be an Integer amount of money.\n")
            else:
                print()
                #return money
        pass
    
    def add(self, record, categories):
        """Add new record.

        Keyword arguments:
        categories  -- an object from Categories
        """
        while(True):
            try:
                assert record != 'q'
                record = record.split()
                [category, desc, amount] = record
                if not categories.is_category_valid(category):
                    record = input("Add an expense or income record with description and an amount:\n")
                    continue
                    #categories.add_categories(category) #TODO EXTRA
                self._record.append(Record(category, desc, amount))
                self._money += int(amount)
            except AssertionError:
                print("Cancel Add Fucntion\n")
                return None #return money, record, categories
            except ValueError: # Exception if can not split into two (desc, amount)
                print("Invalid format.\nFormat: <category> <description> <amount>. e.g.: food breakfast -50\n")
                record = input("Add an expense or income record with description and an amount:\n")
            else:
                print()
                return None

    def view(self):
        """View the whole record.

        Keyword arguments:
        """
        print(f"Here\'s your expense and income records:")
        print(f"{print_Category:<25s} {print_Desc:<25s} {print_Amount:^8s}")
        print("="*25 +" "+ "="*25 + " "+"="*8)
        for data in self._record:
            print(f'{data.category:<25s} {data.name:<25s} {data.amount:>8d}')
        print("="*25 +" "+ "="*25 + " "+"="*8)
        print("Now you have %d dollars.\n" %self._money)
        return

    def delete(self, delete_record):
        """Delete record.

        Keyword arguments:
        delete_record   -- record which you want to delete
        """
        while(True):
            try:
                assert delete_record != 'q'
            except AssertionError:
                print("Cancel Deletion Function\n")
                pass
                #return money, record, categories
            else:
                delete_record = delete_record.split()
                try:
                    if len(delete_record) == 3:
                        del_data = Record(*delete_record);
                        flag = False
                    elif len(delete_record) == 2:
                        del_data = Record(*delete_record, 0);
                        flag = True
                    else : raise TypeError
                except ValueError:
                    print("Invalid format. Amount should be an integer.\n")
                    delete_record = input("Which record do you want to delete? ")
                except TypeError:
                    print("Invalid format. Expect 3 members: <category> <description> <amount>. e.g.: food breakfast -50\n")
                    delete_record = input("Which record do you want to delete? ")
                else:
                    break

        print("\nHere's data found inside in your records:\n")
        print(f"Index\t {print_Category:<25s} {print_Desc:<25s} {print_Amount:^8s}")
        print("="*5 + "\t" + " " + "="*25 + " " + "="*25 + " " + "="*8)

        data_idx_found = []
        found = 0
        for i,data in enumerate(self._record):
            if (data == del_data) if not flag else (data <= del_data):
                found += 1
                print(f"{found:>5d}\t {data.category:<25s} {data.name:<25s} {data.amount:>8d}")
                data_idx_found.append(i)
        print("="*5 + "\t" + " " + "="*25 + " " + "="*25 + " " + "="*8)
        print()
        if found == 0:                 # No data was found
            print(f"Data: {del_data.category:s} {del_data.name:s} "+"{del_data.amount:d} "if flag is False else ""+"not found.")
        elif found == 1:                # Found single, do deletion immediately
            while True:
                confirm = input("Delete the only data (y/n)? ")
                if confirm in ('y','n'):
                    if confirm == 'y':
                        del(self._record[data_idx_found[0]])
                        print("Data id: 1 deleted.")
                        self._money -= del_data.amount
                    break
                else :
                    print("Invalid input! Must be \'y\' or \'n\'.\n")
        else:                                       # Found multiple, do selection, do deletion

            idx = input("Which data index you want to delete? Type \"all\" for all. ")
            if(idx=='all') :
                for m,i in enumerate(data_idx_found):
                    ii=1+i
                    print(f"Data id: {ii} deleted.")
                    del(self._record[data_idx_found(i)-m])
                self._money -= (del_data.amount*(len(data_idx_found)))
            else :
                try:
                    del(self._record[data_idx_found[int(idx)-1]])
                except ValueError:
                    print(f"Invalid index input should be an integer")
                except IndexError:
                    print(f"Index range from 1 to {found:d}\n")
                else:
                    print(f"Data id: {idx} deleted.")
                    self._money -= del_data.amount
                    print()
                    return
        return #return money, record, categories

    def save(self):
        """Write record inside a file.

        Keyword arguments:
        categories  -- the entire category list
        """
        # DEBUG
        #print(record)
        record_pair_list = [(data.category+', '+data.name+', '+str(data.amount)) for data in self._record]
        record_line_list = '\n'.join(record_pair_list)
        
        # Write the data
        try:
            with open("records.txt","w") as fh:
                try:
                    fh.write(f'{self._money}\n')              # write money at first line
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
                return #return (confirm =='y')
    
    def find(self, target_categories):
        """Find record by categories.

        Keyword arguments:
        record      -- the entire record list
        categories  -- the entire category list
        """
        amounts = 0
        print(f"Here\'s your records about {category}:")
        # Headers
        print(f"{print_Category:<25s} {print_Desc:<25s} {print_Amount:^8s}")
        print("="*25 +" "+ "="*25 + " "+"="*8)
        
        for data in filter(lambda x: x.category in target_categories, self._record):
            print(f'{data.category:<25s} {data.name:<25s} {data.amount:>8d}')
            amounts += data.amount
        print("="*25 +" "+ "="*25 + " "+"="*8)
        print(f"The total amount above is {amounts:d} dollars.\n")


class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """Return initialized all category in form of a list.
        Read data in file if available, else request initialize new data.
        """
        def line_to_nested_list(lines, depth=1):
            L=[]
            i=0
            while i<len(lines):
                #print(" "*4*depth+f"{i}{depth}, {lines[i]}", end=' ')
                if lines[i][0]==depth:
                    #print("appended")
                    L.append(lines[i][1])
                elif lines[i][0]>depth:
                    j=i+1
                    while j<len(lines):
                        if lines[j][0]==depth: break
                        j+=1
                    #print("child append")
                    L.append(line_to_nested_list(lines[i:j+1], depth+1))
                    i=j-1
                else: return L
                i+=1
            return L

        # Read Data from a File
        try:
            with open("categories.txt","r") as fh:
                try:
                    #raise ValueError
                    lines = list(map(lambda x: (int(x.split()[0]), x.split()[1]), fh.readlines()))
                    self._categories = line_to_nested_list(lines)
                except AssertionError:
                    print("Recorded file is an empty file.\n")
                    self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]  
                except ValueError:      # Exception: File first line not an Integer
                    print("Fail to read the recorded file.\n")
                    self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]  
                else:                   # Read data to the record variable
                    pass
        except FileNotFoundError:       # Exception: File did not exist
            self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]  
        return 
    def add(self, category, parent=''):
        """Adding a category on a category list"""

        def rec_find(L, val):
            if type(L) in {list, tuple}: # if look inside members of L
                for i, v in enumerate(L):
                    p = rec_find(v, val) # recursively find each member
                if p == True: # L[i] == val, so we return (i,)
                    return (i,)
                if p != False: # L[i] recursively found val, 
                    return (i,)+p # so we prepend i to its path p
            return L == val # either L is not seq or for-loop didn't find

        if parent == '':
            self._categories.append(category)
            return
        if not self.is_category_valid(parent):
            print("The parent cannot be found. Failed adding new category!\n")
        
        catt = self._categories
        for id in rec_find(self._categories, parent):
            catt = catt[id]
        catt.append(category)
        pass
            

    def find_subcategories(self, category):
        """Return all subcategories of a category as a list.ad
        Return empty list [] if no category is found.

        Keyword arguments:
        category    -- the searched category
        """
        def find_subcategories_gen(category, categories, found=False):
            """Generator search specific item in nested list, return flatten list. """
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index+1], True)
            else:
                if categories == category or found == True:
                    yield categories

        # Return generated list
        return [x for x in find_subcategories_gen(category, self._categories)]

    def is_category_valid(self, category):
        """Return True if a category is exist inside the category list.
        Otherwise, return False.

        Keyword arguments:
        categories  -- the entire category list
        category    -- the searched category
        """
        if type(category) in {list, tuple}: # Only has one value
            for cat in category:
                return self.is_category_valid(cat)
        
        return False if self.find_subcategories(category) == [] else True

    def view(self, L ,depth=0):
        """Print all the whole category list.

        Keyword arguments:
        categories  -- the entire category list
        depth       -- the depth occur recursively (default = 0)
        """
        if depth == 0: print("Category: ")
        for i, atom in enumerate(L):
            if type(atom) not in {list, tuple}:
                print(' '*4*depth + '- ' + atom)
            else :
                self.view(atom, depth+1)
            # depth+'.'+str(i+1) if depth else str(i+1)   
        if depth ==0: print()
    
    def save(self):
        def list_depth_gen(categories = self._categories, depth=1):
            txt = ''
            for atom in categories:
                if type(atom) != list:
                    txt = f"{depth:d} {atom:s}\n"
                    yield txt
                else :
                    yield from list_depth_gen(atom, depth+1)
            return
        with open("categories.txt", "w") as fh:
            for line in list_depth_gen(self._categories):
                fh.write(line)
            



# Global Function
def input_command():
    """Input command to do error control.
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


# Class Definitions
categories = Categories()
records = Records()

# Main Program
while True:
    command = input_command()
    if command == 'add':
        record = input("Add an expense or income record with description and an amount:\n")
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? ")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view(categories._categories)
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        categories.save()
        break
    elif command == 'add categories':
        category = input('Whats the name of your new category? ') 
        parent = input('Where this new category branching from? (type \"main\" if want to be the main category) ') 
        categories.add(category, parent if parent!='main' else '')
    else:
        sys.stderr.write('Invalid command. Try again.\n')
