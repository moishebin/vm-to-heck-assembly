import argparse
from fileParser import FileParser
from CodeWriter import CodeWriter


class VMTranstalor:
    def __init__(self, filename):
        self.filename = filename
        file_parser = FileParser(filename)
        vmcode = file_parser.readline(filename)
        code_writer = CodeWriter(filename)
        for line in vmcode:
            code_writer.translate(line)


        
        
        



if __name__ == '__main__':

    arg = argparse.ArgumentParser()
    arg.add_argument("input_file", help="path to input file")
    args = arg.parse_args()
    vm = VMTranstalor(filename = args.input_file)

