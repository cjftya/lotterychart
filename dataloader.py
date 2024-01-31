import pandas as pd
import matplotlib.pyplot as plt
import os

class DataLoader:
    def __init__(self):
        data = pd.read_csv("lottodata.csv", encoding="cp949")
        self.result = data.iloc[2:,:]
        self.numberDataArray = dict()
        print("init")


    def getNormalData(self, originArr):
        arr = []
        index = []
        size = len(originArr[1])
        for i in range(size):
            if originArr[1][i] == -1:
                continue
            index.append(originArr[0][i])
            arr.append(originArr[1][i] + 1)
        return [index, arr]


    def getDensityData(self, originArr, sildingSize):
        arr = []
        index = []
        size = len(originArr[1])
        halfSlidingSize = sildingSize / 2
        for i in range(size):
            acc = 0
            start = int(i - halfSlidingSize)
            start = start if start >= 0 else 0
            end = int(i + halfSlidingSize)
            end = end if end < size else size
            for k in range(start, end):
                if originArr[1][k] != -1:
                    if k < i:
                        acc += 1
                    else:
                        acc += 2

            arr.append((acc * 100) / sildingSize)
            index.append(originArr[0][i])

        return [index, arr]
    

    def getPositionDensityData(self, originArr, sildingSize):
        posArrSet = []
        postIndexSet = []
        size = len(originArr[1])
        halfSlidingSize = sildingSize / 2
        for p in range(6):
            posIndex = []
            posArr = []
            for i in range(size):
                acc = 0
                start = int(i - halfSlidingSize)
                start = start if start >= 0 else 0
                end = int(i + halfSlidingSize)
                end = end if end < size else size
                for k in range(start, end):
                    if originArr[1][k] == p:
                        acc += 1

                posArr.append((acc * 100) / sildingSize)
                posIndex.append(originArr[0][i])

            posArrSet.append(posArr)
            postIndexSet.append(posIndex)

        return [postIndexSet, posArrSet]
    

    def draw(self, selectedNum, isSave=False, isShow=True):
        if len(self.numberDataArray) == 0:
            print("empty data")

        data = self.numberDataArray[selectedNum]
        normalData = data["normal"]
        densityData = data["density"]
        posDensityData = data["pos"]
        plt.subplot(3, 1, 1)
        plt.plot(normalData[0], normalData[1], "b.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Confirm " + str(selectedNum))

        densityDataSize = len(densityData[0]);
        plt.subplot(3, 1, 2)
        plt.plot(densityData[0], densityData[1], "b.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Density " + str(selectedNum) + " (" + str(densityData[1][densityDataSize-1]) + "%)")

        plt.subplot(3, 1, 3)
        plt.plot(posDensityData[0][0], posDensityData[1][0], "b.-", 
                posDensityData[0][1], posDensityData[1][1], "r.-",
                posDensityData[0][2], posDensityData[1][2], "g.-",
                posDensityData[0][3], posDensityData[1][3], "c.-",
                posDensityData[0][4], posDensityData[1][4], "k.-",
                posDensityData[0][5], posDensityData[1][5], "m.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Pos " + str(selectedNum) + " (B:1, R:2, G:3, C:4, K5, M6)")

        plt.tight_layout()
        if isSave:
            dirName = "figure"
            if not os.path.exists(dirName):
                os.mkdir(dirName)
            # else:
            #     print("already exist")

            figure = plt.gcf() # get current figure
            figure.set_size_inches(15, 10)
            plt.savefig(dirName + "/pic" + str(selectedNum) + ".png", dpi=100, bbox_inches='tight')

        if isShow:
            plt.show()

        plt.clf()


    def printData(self, selectedNum):
        print()
        print("---------------------------------")

        if len(self.numberDataArray) == 0:
            print("empty data")

        data = self.numberDataArray[selectedNum]
        densityData = data["density"]
        posDensityData = data["pos"]
        print("density " + str(densityData[1][len(densityData[1]) - 1]) + "%")
        for i in range(6):
            print("pos(" + str(i+1) + ") " +
                   str(posDensityData[1][i][len(posDensityData[1][i]) - 1]))
        
        print("---------------------------------")
        print()

    def printRating(self, position):
        print()
        print("---------------------------------")
        print("# position " + str(position))
        rateArray = []
        for i in range(1, 46):
            densityData = self.numberDataArray[i]["density"]
            posData = self.numberDataArray[i]["pos"]
            r1 = densityData[1][len(densityData[1]) - 1]
            r2 = posData[1][position - 1][len(posData[1][position - 1]) - 1]
            result = r1 + r2 if r2 > 0 else 0
            rateArray.append([result, i])
        rateArray.sort(key=lambda x: -(x[0]))
        
        for i in range(len(rateArray)):
            data = rateArray[i]
            print(" > " + str(data[1]) + " : " + str(round(data[0], 3)) + "%")
        
        print("---------------------------------")
        print()

    
    def loadAll(self):
        for i in range(1, 46):
            self.load(i)


    def getParsedArray(self, obj):
        return [int(obj[0]), int(obj[1]), int(obj[2]),
                int(obj[3]), int(obj[4]), int(obj[5]),
                int(obj[6])]


    def load(self, selectedNum):
        fullArr = []
        fullIndex = []
        size = len(self.result) - 1

        for i in range(size, -1, -1):
            fIndex = self.findPosition(self.getParsedArray(self.result.iloc[i,13:20]), selectedNum)
            fullArr.append(fIndex)
            fullIndex.append(int(self.result.iloc[i,1]))

        fullData = [fullIndex, fullArr]
        normalData = self.getNormalData(fullData)
        densityData = self.getDensityData(fullData, 50)
        posDensityData = self.getPositionDensityData(fullData, 300)

        self.numberDataArray[selectedNum] = {"full":fullData, "normal":normalData, "density": densityData, "pos": posDensityData}


    def findPosition(self, arr, num):
        for i in range(len(arr)):
            if num == arr[i]:
                if i == 6:
                    return -1
                return i
        return -1
    

