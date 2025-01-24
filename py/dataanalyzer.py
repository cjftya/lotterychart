class DataAnalyzer:
    def __init__(self):
        print("init")


    def analyzePredictFirst(self, dataSet):
        print("analyzePredictFirst")
        st = len(dataSet) - 300
        ed = len(dataSet)

        arr = []
        for i in range(st, ed):
            data = dataSet[i]
            if data.getNumber(0) == '10':
                nextNum = dataSet[i + 1].getNumber(0)
                arr.append(nextNum)
        
        print(arr)


    def analyze(self, dataSet):
        st = len(dataSet) - 100
        ed = len(dataSet)
        print(dataSet[st].getDate() + " ~ " + dataSet[ed - 2].getDate())

        nlist = [dict(), dict(), dict(), dict(), dict(), dict()]
        for i in range(st, ed):
            data = dataSet[i]
            for j in range(6):
                nset = nlist[j]
                nset[data.getNumber(j)] = nset.get(data.getNumber(j), 0) + 1

        numberSet = [[], [], [], [], [], []]
        for i in range(6):
            for v in sorted(nlist[i].items(), key=lambda x: x[1], reverse=True):
                if v[1] >= 4:
                    numberSet[i].append(int(v[0]))
        
        for i in range(6):
            numberSet[i] = sorted(numberSet[i], reverse=False)

        caseSet = []
        for n1 in numberSet[0]:
            for n2 in numberSet[1]:
                for n3 in numberSet[2]:
                    for n4 in numberSet[3]:
                        for n5 in numberSet[4]:
                            for n6 in numberSet[5]:
                                if n1 < n2 < n3 < n4 < n5 < n6:
                                    caseSet.append((n1, n2, n3, n4, n5, n6))

        print(len(caseSet))
        # for s in caseSet:
        #     print(s)

        # print(sorted(nlist[0].items(), key=lambda x: x[1], reverse=True))
        # for i in range(6):
        #     print(f"{i + 1}>")
        #     print(sorted(nlist[i].items(), key=lambda x: x[1], reverse=True))
        #     print()