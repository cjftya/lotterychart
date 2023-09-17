from prophet import Prophet
from prophet.plot import add_changepoints_to_plot

from dataloader import DataLoader

dataLoader = DataLoader()

if __name__ == "__main__":
    dataLoader.load(2)
    # for i in range(1, 46):
    #     dataLoader.load(i)
