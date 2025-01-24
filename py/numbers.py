class Numbers:
    def __init__(self, data):
        self.n = data[0]
        self.date = data[1]
        self.numbers = data[2:]


    def getNo(self):
        return self.n
    

    def getDate(self):
        return self.date
    

    def getNumbers(self):
        return self.numbers
    

    def getNumber(self, idx):
        return self.numbers[idx]