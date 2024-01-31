from dataloader import DataLoader

dataLoader = DataLoader()

if __name__ == "__main__":
    dataLoader.loadAll()
    for i in range(6):
        dataLoader.printRating(i + 1)

    # for i in range(1, 46):
    #     dataLoader.draw(i, isSave=True, isShow=False)
