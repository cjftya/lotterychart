from prophet import Prophet
from prophet.plot import add_changepoints_to_plot

from dataloader import DataLoader

dataLoader = DataLoader()

if __name__ == "__main__":
    dataLoader.loadAll()
    dataLoader.printData(2)
    dataLoader.draw(2)
