# extract function declaration (ex. int foo(int a, char b) from 
# input C source code and output func list to a file)

import argparse

def parse_from_file(input_file, funclist=set()):
    line = " "
    count = 0 # to know which line we are parsing
    while line:
        # read line from source code
        line = input_file.readline()
        if not line:
            break
        count += 1
        #print(f"[{count}]")
        #print(f"input line: {line}")
        if line.startswith(" ") or line.startswith("\t") or line.startswith("/") or line.startswith("#") \
           or line.startswith("\n") or line.startswith("{") or line.startswith("}") or line.startswith("*")\
           or line.find(":") > 0 : # ":" is to remove tag
            # ignore these lines
            pass
        elif line.startswith("extern"): # remove extern to avoid duplicating in result
            print(f"starts with extern:{line}")
            line = line.strip("extern")
        else:
            #print(f"parse raw line: {line}")
            semicolon = line.find(";")
            end = line.rfind(")") # find from the end to deal with function pointer argument correctly
        
            # find till there are ";" or ")". If no ";" or ")" concatenate the line with next line
            while semicolon < 0 and end < 0:
                line_cont = input_file.readline().strip(" \t")
                count += 1
                #print(f"[{count}]")
                line = line.strip('\n') + line_cont
                semicolon = line.find(";")
                end = line.rfind(")")

            # ignore only semicolon line (it is not a function)        
            #print(f"parse joined line: {line}")
            if end > 0:
                if line[0:end + 1] in funclist:
                    pass # func is already in the list
                elif line.startswith("static"):
                    pass # do not include static func in list
                else:
                    #print(f'{line[0:end + 1]} is func')
                    funclist.add(line[0:end + 1])
    print(funclist)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "argParser")

    parser.add_argument('inputFile', help = 'input file path')
    parser.add_argument('outputFile', help = 'output file path')
    args = parser.parse_args()

    funclist = set() 
    with open(args.inputFile) as input_file:
        parse_from_file(input_file, funclist)

    with open(args.outputFile, 'w') as output_file:
        for func in funclist:
            output_file.write(func + '\n')
