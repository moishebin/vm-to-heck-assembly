import os


class CodeWriter:
    def __init__(self, filename):
        self.filename = os.path.splitext(filename)[0]
        self.basename = filename = os.path.basename(self.filename)
        self.writefile = open(self.filename + '.asm', 'w')
        self.arguments= {
        "local" : "@LCL \n",
        "argument" : "@ARG \n",
        "this" : "@THIS \n",
        "that" : "@THAT \n"
        }
        self.count = 0
    def write(self, line):
        self.writefile.write(line + '\n')
    def close(self):
        self.writefile.close()
    
    def translate(self, line):
        
        # write original code line
        self.write("//" + line.replace('\n', ''))

        #translate code
        line = line.split()
        if line[0] == "push":
            self.push(line[1], int(line[2]))
        elif line[0] == "pop":
            self.pop(line[1], int(line[2]))
        else:
            self.arithmetic(line[0])


    def push(self, arg1, num):

        stack = "@SP \nA=M \nM=D \n@SP \nM=M+1 \n"
        asmPvalue = f"D=M \n@{num} \nA=D+A \nD=M \n"

        if arg1 == "constant":
            self.write(f'@{num} \nD=A \n{stack}')
        elif arg1 == "static":
            self.write(f'@{self.basename + "." + str(num)}\nD=M \n{stack}')
        elif arg1 == "temp":
            self.write(f'@{5 + num} \nD=M \n{stack}')
        elif arg1 == "pointer":
            self.write(f'@{3 + num} \nD=M \n{stack}')
        else:
            self.write(self.arguments[arg1] + asmPvalue + stack)

    def pop(self, arg1, num):
        stack = "@SP \nM=M-1 \n@SP \nA=M \nD=M \n"

        if arg1 == "pointer":
            self.write( f'{stack}@{3 + num} \nM=D \n')
        elif arg1 == "temp":
            self.write( f'{stack}@{5 + num} \nM=D \n')
        elif arg1 == "static":
            self.write( f'{stack}@{self.basename + "." + str(num)} \nM=D \n')
        else:
            self.write(f'{self.arguments[arg1]}AD=M \n@{num} \nD=D+A \n@R13 \nM=D \n{stack}@R13 \nA=M \nM=D \n')

    
    def arithmetic(self, arg):
        operator = {
            'add':'+',
            'sub':'-',
            'or':'|',
            'and':'&',
        }
        neg = {
            'not':'!',
            'neg':'-'
        }
        condition = {
            'eq':'JEQ',
            'lt':'JLT',
            'gt':'JGT'
        }
        if arg in operator:
            self.write(f"@SP \nM=M-1 \n@SP \nA=M-1 \nD=M \n@SP \nA=M \nD=D{operator[arg]}M \n@SP \nA=M-1 \nM=D \n")
        elif arg in neg:
            self.write(f"@SP \nM=M-1 \n@SP \nA=M \nD={neg[arg]}M \n@SP \nA=M-1 \nM=D \n")
        elif arg in condition:
            self.write(f"@SP \nM=M-1 \nA=M \nD=M \n@SP \nA=M-1 \nD=D-M \n@Correct{self.count} \nD;{condition[arg]} \n@SP \nA=M-1 \nM=0 \n@Done{self.count} \n0;JMP \n(Correct{self.count}) \n@SP \nA=M \nM=-1 \n(Done{self.count})\n@SP \nM=M+1 \n")
            self.count += 1
 

        
   