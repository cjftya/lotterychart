import pandas as pd
import matplotlib.pyplot as plt
import os

class DataLoader:
    def __init__(self):
        data = pd.read_csv("lottodata.csv", encoding="cp949")
        self.result = data.iloc[:,0:8]
        self.numberDataArray = dict()
        print("init")


    def getNormalData(self, originArr):
        arr = []
        index = []
        size = len(originArr[1])
        for i in range(size):
            if originArr[1][i] == 0:
                continue
            index.append(originArr[0][i])
            arr.append(originArr[1][i])
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
                if originArr[1][k] != 0:
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
                    if originArr[1][k] == p + 1:
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

        plt.subplot(3, 1, 2)
        plt.plot(densityData[0], densityData[1], "b.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Density " + str(selectedNum))

        plt.subplot(3, 1, 3)
        plt.plot(posDensityData[0][0], posDensityData[1][0], "b.-", 
                posDensityData[0][1], posDensityData[1][1], "r.-",
                posDensityData[0][2], posDensityData[1][2], "g.-",
                posDensityData[0][3], posDensityData[1][3], "c.-",
                posDensityData[0][4], posDensityData[1][4], "k.-",
                posDensityData[0][5], posDensityData[1][5], "m.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Pos " + str(selectedNum))

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
        if len(self.numberDataArray) == 0:
            print("empty data")

        data = self.numberDataArray[selectedNum]
        densityData = data["density"]
        posDensityData = data["pos"]
        print("density " + str(densityData[1][len(densityData[1]) - 1]) + "%")
        for i in range(6):
            print("pos(" + str(i+1) + ") " +
                   str(posDensityData[1][i][len(posDensityData[1]) - 1]))

    
    def loadAll(self):
        for i in range(1, 46):
            self.load(i)


    def load(self, selectedNum):
        fullArr = []
        fullIndex = []
        size = len(self.result) - 1
        for i in range(size, -1, -1):
            fIndex = self.findPosition(self.result.iloc[i,:], selectedNum)
            fullArr.append(fIndex)
            fullIndex.append(self.result.iloc[i,0])

        fullData = [fullIndex, fullArr]
        normalData = self.getNormalData(fullData)
        densityData = self.getDensityData(fullData, 50)
        posDensityData = self.getPositionDensityData(fullData, 300)

        self.numberDataArray[selectedNum] = {"full":fullData, "normal":normalData, "density": densityData, "pos": posDensityData}


    def findPosition(self, arr, num):
        for i in range(1, len(arr)):
            if num == arr[i]:
                if i == 7:
                    return 0
                return i
        return 0
    

