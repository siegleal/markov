import random

class markov:

    def __init__(self):
        self.dict = {}
        self.prefixLength = 1
        self.deleteNewline = True

    def setPrefixLength(self, l):
        if l >= 1:
            self.prefixLength = l
            self.dict = {}
    def setDeleteNewline(self, b):
        self.deleteNewline = b

    def formatNewline(self, s):
        return s.replace('<newline>','\n')

    def produce(self, numWords):
        result = self.chooseNext('^').split(' ')
        for i in range(self.prefixLength, numWords):
            last = result[-self.prefixLength:]
            newWord = self.chooseNext(' '.join(last))
            if newWord == '^': #special case because ^ give a full prefix result
                newWords = self.chooseNext('^').split(' ')
                for i in range(0, len(newWords)):
                    result.append(newWords[i])
            else:
                result.append(newWord)
        return self.formatNewline(' '.join(result))

    def trainFromFile(self, filepath):
        f = open(filepath, 'r')
        nextLine = f.readline()
        while (nextLine != ''):
            self.train(nextLine)
            nextLine = f.readline()

    def train(self, input):
        #format input
        #add a space beforecommas so it's its own word
        if self.deleteNewline:
            input = input.replace('\n','')
        else:
            input = input.replace('\n', '<newline>')
        input = input.replace(',',' ,').replace('.',' .').replace('?',' ?').replace('!',' !').replace('!',' !')
        input = input.replace('(','').replace(')','').replace('"','').lower()

        inputArr = input.split(" ")
        if len(inputArr) <= self.prefixLength:
            return
        for i in range(self.prefixLength, len(inputArr)):
            key = inputArr[i-self.prefixLength:i]
            self.appendTo(' '.join(key), inputArr[i])

        #priming
        self.appendTo('^', ' '.join(inputArr[0:self.prefixLength]))
        self.appendTo(' '.join(inputArr[-self.prefixLength:]), '^')

    def appendTo(self, before, after):
        if self.dict.has_key(before): #we have seen this root word before
            entry = self.dict[before]
            if after in entry[0]: #we have seen this word pair before
                entry[1][entry[0].index(after)] += 1
            else: # we have not seen this word pair before
                entry[0].append(after)
                entry[1].append(1) #begin with one sighting
        else: #we have not seen this root word before
            self.dict[before] = ([after],[1])

    def getTotal(self, before):
        return sum(self.dict[before][1])

    def buildChoices(self, before):
        result = []
        entry = self.dict[before]
        wordList = entry[0]
        occurence = entry[1]
        for x in range(0, len(wordList)):
            for y in range(0,occurence[x]):
                result.append(wordList[x])
        return result

    def chooseNext(self, before):
        choice = random.choice(self.buildChoices(before))
        return choice

    def printEntry(self,entry):
        result = ''
        for x in range(0,len(entry[0])):
            result += "\t" + str(entry[1][x])+ ': ' + str(entry[0][x]) + '\n'
        return result

    def printDict(self):
        result = ''
        for before in self.dict:
            result += before + ': ' + str(self.getTotal(before)) +'\n'
            result += self.printEntry(self.dict[before])
        return result

############end class################
def test():
    m = markov()
    m.appendTo('hello','world')
    m.appendTo('hello', 'one')
    m.appendTo('hello', 'two')
    m.appendTo('hello', 'two')
    print m.printDict();
    c = m.buildChoices('hello')
    print c
    print m.chooseNext('hello')
    print '=========='
    m = markov()
    m.train('The quick brown fox jumps over the lazy dog. Hello World!')
    print m.printDict();
    print m.produce(30)
    print '=========='
    m = markov()
    m.trainFromFile("C:\\Users\\Andrew\\Desktop\\markov\\a7x.txt")
    print m.produce(50)
    print '=========='
    m = markov()
    m.setPrefixLength(2)
    m.setDeleteNewline(True)
    m.trainFromFile("C:\\Users\\Andrew\\Desktop\\markov\\a7x.txt")
    print m.produce(50)
    #print m.printDict()

