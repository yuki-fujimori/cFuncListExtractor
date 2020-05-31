import argparse
import glob
import cFuncListExtractor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "argParser")

    parser.add_argument('inputDirectory', help = 'input directory path')
    args = parser.parse_args()

    files = glob.glob(args.inputDirectory + "/**/*.c") # sub directories
    cd_files = glob.glob(args.inputDirectory + "/*.c") # Current directory 
    for file in cd_files:
        files.append(file)
    file_set = set(files) # remove if duplicated files are in the list
    for file in file_set:
        funclist = []
        with open(file) as input_file:
            cFuncListExtractor.parse_from_file(input_file, funclist)

        with open("./output.txt", 'a+') as output_file:
            for func in funclist:
                output_file.write(func + '\n')