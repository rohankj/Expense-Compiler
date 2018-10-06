import re
import operator

categories = {}
misc = {}
spending = {}


def add_amount(category, amount, array):
    if ( category in array ):
         array[category] += float(amount)
    else:
        array[category] = float(amount)
    return
        
def calculate_spending(description, amount):
    my_amount = re.sub(r"\s|\$|,", "", amount)
    myFlag = False
    
    for k, v in categories.items():
        my_pattern = r"" + re.escape(k) + r""
        
        searchObj = re.search( my_pattern , description, re.IGNORECASE)
        
        if(searchObj):
            add_amount(v, my_amount, spending)
            myFlag = True
            break

    if ( myFlag == False):
        my_pattern = r"" + re.escape("refund") + r""
        
        creditObj1 = re.search( my_pattern, description, re.IGNORECASE)

        my_pattern = r"" + re.escape("REDEMPTION CREDIT") + r""

        creditObj2 = re.search( my_pattern, description, re.IGNORECASE)
        
        if(creditObj1 or creditObj2):
            my_amount = "-" + my_amount            
            add_amount("Miscellaneous", my_amount, spending)
        else:
            add_amount("Miscellaneous", my_amount, spending)
            add_amount(description, my_amount, misc)
        
    return        


######################################################
# Store the Categories file into an associative array
######################################################
with open('D:\Personal\Python\Categories.txt', 'r') as infile:
    # Read the contents of the file into memory.
    data = infile.read()  

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

for line in my_list:
    splitstr = line.split("\t")
    categories[splitstr[0]] = splitstr[1]

#print(categories)

######################################################
# Process the Citi file
######################################################
with open('D:\Personal\Python\\citi_2018.txt', 'r') as infile:
    # Read the contents of the file into memory.
    data = infile.read()  

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

for line in my_list:
    splitstr = line.split("\t")
    if(len(splitstr[1]) != 0):
        #print("value1 = " + splitstr[0] + ", value2 = " + splitstr[1])
        calculate_spending(splitstr[0], splitstr[1])
        
infile.close()
    

######################################################
# Process the Bofa file
######################################################
with open('D:\Personal\Python\\bofa_2018.txt', 'r') as infile:
    # Read the contents of the file into memory.
    data = infile.read()  

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

for line in my_list:
    splitstr = line.split("\t")
    if(len(splitstr[4]) != 0 and float(splitstr[4]) < 0):
        #print("value1 = " + splitstr[0] + ", value2 = " + splitstr[1])
        calculate_spending(splitstr[2], splitstr[4].replace("-", ""))    

infile.close()

######################################################
# Process the Discover file
######################################################
with open('D:\Personal\Python\\discover_2018.txt', 'r') as infile:
    # Read the contents of the file into memory.
    data = infile.read()  

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

for line in my_list:
        if(line.find("DIRECTPAY") == -1):    
            splitstr = line.split("\t")
            calculate_spending(splitstr[2], splitstr[3])    

infile.close()

######################################################
# Process the Chase file
######################################################
with open('D:\Personal\Python\\chase_2018.txt', 'r') as infile:
    # Read the contents of the file into memory.
    data = infile.read()  

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

for line in my_list:
        if(line.find("AUTOMATIC PAYMENT") == -1):    
            splitstr = line.split("\t")
            calculate_spending(splitstr[0], splitstr[1])

infile.close()

print("======================================================================================\n")

sorted_spending = sorted((val, key) for key, val in spending.items())

#for k, v in spending.items():
    #buf = "Description = %s, Amount = %.2f" % (k, v)
    #print (buf)

############################################################
# print the spending array in reverse order of values
############################################################
for key, value in sorted(spending.items(), key=lambda item: (item[1], item[0]), reverse=True):
    buf = "Description = %s, Amount = %.2f" % (key, value)
    print (buf)
    
print("\n====================================================================================\n")

for k, v in misc.items():
    buf = "Description = %s, Amount = %.2f" % (k, float(v))
    print (buf)

print("\n======================================================================================")

