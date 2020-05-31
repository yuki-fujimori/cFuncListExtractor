# input function declaration list(cab be made from cFuncListExtractor.py) 
# and output FAKE_XX_FUNC list which can be used in Fake Function Framework
# Also output REESET_FAKE list which can be used in SetUp() of test fixture

import argparse

class Arg:
    def __init__(self, name, arg_type):
        self.name = name
        self.type = arg_type

class Func:
    def __init__(self, name, ret_type, args):
        self.name = name
        self.ret_type = ret_type.strip(" ")
        self.args = args.copy() 
    def outputFakeSource(self):
        arg_str = ""
        for arg in self.args:
            arg_str += arg.type
            arg_str += ", "
        arg_str = arg_str.rstrip(", ")
        if self.ret_type == "void":
            return "FAKE_VOID_FUNC(" + self.name + ", " + arg_str + ");\n"
        else:
            return "FAKE_VALUE_FUNC(" + self.ret_type + ", "  + self.name + ", " + arg_str + ");\n"
    def outputResetFake(self):
        return "RESET_FAKE(" + self.name + ");\n"
    
def parse_from_file(input_file, funclist=[]):
    arglist = []
    line = " "
    count = 0
    while line:
        # each line contains one Func declaration
        line = input_file.readline()
        if not line:
            break
        count += 1
        print(f"[{count}]")
        print(f"parse raw line: {line}")

        # separate line to tow block
        # before: ret_type func_name
        # after: args
        blocks = line.split("(")
        before = blocks[0]
        after = ""
        for blk in blocks[1:]:
            after = after + blk + "("
        after = after.rstrip("(")
        after = after.rstrip("\n")
        after = after.rstrip(")")
        print(f"before:{before} \nafter:{after}")

        #separate befor to ret_type & func_name
        before_blks = before.split(" ")
        func_name = before_blks[-1]
        pointer_flag = False
        if func_name.startswith("*"):
            func_name = func_name.strip("*")
            pointer_flag = True
        print(f"func_name: {func_name}")
        ret_type = ""
        for blk in before_blks[0:-1]:
            ret_type = ret_type + blk + " "
        if pointer_flag == True:
            ret_type += "*"
        print(f"ret_type: {ret_type}")

        #separate after to list of Arg class[arg_type & arg_name]
        args_blks = after.split(",")
        for arg in args_blks:
            arg_blks = arg.split(" ")
            arg_name = arg_blks[-1]
            pointer_flag = False
            if arg_name.startswith("*"):
                arg_name = arg_name.strip("*")
                pointer_flag = True
            print(f"arg_name: {arg_name}")
            arg_type = ""
            for blk in arg_blks[0:-1]:
                arg_type = arg_type + blk + " "
            if pointer_flag == True:
                arg_type += "*"
            arg_type = arg_type.strip(" ")
            print(f"arg_type: {arg_type}")
            
            tmp_arg = Arg(arg_name, arg_type)
            arglist.append(tmp_arg)
        
        # append Func class to funclist
        tmp_func = Func(func_name, ret_type, arglist)
        funclist.append(tmp_func)
        arglist.clear()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "argParser")

    parser.add_argument('inputFile', help = 'input file path(Func Declaration file)')
    parser.add_argument('outputFile', help = 'output file path(Fake Output file)')
    args = parser.parse_args()

    funclist = []
    with open(args.inputFile) as input_file:
        parse_from_file(input_file, funclist)

    with open(args.outputFile, 'w') as output_file:
        for func in funclist:
            output_file.write(func.outputFakeSource()) 
        output_file.write("\n")
        for func in funclist:
            output_file.write(func.outputResetFake())