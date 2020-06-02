import argparse
import glob
import cFuncListExtractor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "argParser")

    parser.add_argument('inputDirectory', help = 'input directory path')
    parser.add_argument('depth', help = 'target subdirectory depth')
    args = parser.parse_args()

    file_set = set() 
    for i in range(int(args.depth)):
        depth_str = "/**"
        files = glob.glob(args.inputDirectory + depth_str * i + "/*.c")
        for file in files:
            file_set.add(file)

    for file in file_set:
        print(file)
    
    funcset = set()
    for file in file_set:
        funclist = set() 
        with open(file) as input_file:
            cFuncListExtractor.parse_from_file(input_file, funclist)

        for func in funclist:
            funcset.add(func) # remove duplicate here
    
    with open("./funclist.txt", 'w') as output_file:
        for func in funcset:
            output_file.write(func + '\n')
