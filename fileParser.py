import os

class FileParser:
    def __init__(self, fileName):
        self.filename = fileName


    def open(self, fileName):
        extension = os.path.splitext(self.filename)[1]
        if extension == '.vm':
            self.file = open(fileName, 'r')
            return self.file
        else:
            try:
                self.file = open(fileName + '.vm', 'r')
                return self.file
            except:
                print('File not found')
                return
    

    def readline(self, filename):
        self.file = self.open(filename)
        self.line = self.file.readlines()
        self.code = []
        for line in self.line:
            if line.strip() != "" and not line.strip().startswith("//"):
                self.code.append(line)
        self.file.close()
        return self.code
        
     