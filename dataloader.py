import pandas as pd
import matplotlib.pyplot as plt

class DataLoader:
    def __init__(self):
        data = pd.read_csv("lottodata.csv", encoding="cp949")
        self.result = data.iloc[:,0:8]
        print("init")
    
    def load(self, selectNum):
        fullArr = []
        fullIndex = []
        arr = []
        index = []
        size = len(self.result) - 1
        selectedNum = selectNum
        for i in range(size-0, -1, -1):
            fd = self.findPosition(self.result.iloc[i,:], selectedNum)
            fullArr.append(fd)
            fullIndex.append(self.result.iloc[i,0])

            if fd == 0:
                continue
            arr.append(fd)
            index.append(self.result.iloc[i,0])


        densitySlidingSize = 50
        halfDensitySlidingSize = densitySlidingSize / 2
        densityIndex = []
        densityArr = []
        for i in range(0, len(fullArr)):
            acc = 0
            start = int(i - halfDensitySlidingSize)
            start = start if start >= 0 else 0
            end = int(i + halfDensitySlidingSize)
            end = end if end < len(fullArr) else len(fullArr)
            for k in range(start, end):
                if fullArr[k] != 0:
                    if k < i:
                        acc += 1
                    else:
                        acc += 2

            densityArr.append((acc * 100) / densitySlidingSize)
            densityIndex.append(fullIndex[i])

        
        posArrSet = []
        postIndexSet = []
        posSlidingSize = 300
        halfPosSlidingSize = int(posSlidingSize / 2)
        for p in range(6):
            posIndex = []
            posArr = []
            for i in range(0, len(fullArr)):
                acc = 0
                start = int(i - halfPosSlidingSize)
                start = start if start >= 0 else 0
                end = int(i + halfPosSlidingSize)
                end = end if end < len(fullArr) else len(fullArr)
                for k in range(start, end):
                    if fullArr[k] == p + 1:
                        acc += 1

                posArr.append((acc * 100) / posSlidingSize)
                posIndex.append(fullIndex[i])

            posArrSet.append(posArr)
            postIndexSet.append(posIndex)


        plt.subplot(3, 1, 1)
        plt.plot(index, arr, "b.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Confirm " + str(selectedNum))

        plt.subplot(3, 1, 2)
        plt.plot(densityIndex, densityArr, "b.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Density " + str(selectedNum))

        plt.subplot(3, 1, 3)
        plt.plot(postIndexSet[0], posArrSet[0], "b.-", 
                 postIndexSet[1], posArrSet[1], "r.-",
                 postIndexSet[2], posArrSet[2], "g.-",
                 postIndexSet[3], posArrSet[3], "c.-",
                 postIndexSet[4], posArrSet[4], "k.-",
                 postIndexSet[5], posArrSet[5], "m.-")
        plt.grid(True)
        plt.tick_params(axis='both', direction='in', length=3, pad=3)
        plt.title("Pos " + str(selectedNum))

        plt.tight_layout()
        # figure = plt.gcf() # get current figure
        # figure.set_size_inches(15, 10)
        # plt.savefig("figure/pic" + str(selectedNum) + ".png", dpi=100, bbox_inches='tight')
        # plt.clf()
        plt.show()


    def findPosition(self, arr, num):
        for i in range(1, len(arr)):
            if num == arr[i]:
                if i == 7:
                    return 0
                return i
        return 0


