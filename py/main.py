from dataloader import DataLoader
from dataanalyzer import DataAnalyzer

dataLoader = DataLoader()
dataAnalyzer = DataAnalyzer()

if __name__ == "__main__":
    dataLoader.load()
    dataLoader.info()
    dataAnalyzer.analyze(dataLoader.getData())
    # dataAnalyzer.analyzePredictFirst(dataLoader.getData())


