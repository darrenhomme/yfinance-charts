import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

class Object(object):
    pass

def CalcPercent(ticker, cpi, index):
    inflation = 0
    first     = float(ticker.history['Close'][0])
    now       = float(ticker.history['Close'][index])
    dividends = float(sum(ticker.history['Dividends'][0:index]))

    # Adjust the return by the cpi data
    if cpi:
        if index > len(cpi.history['Close'])-1:
            index = len(cpi.history['Close'])-1
        firstCpi     = float(cpi.history['Close'][0])
        nowCpi       = float(cpi.history['Close'][index])
        dividendsCpi = float(sum(cpi.history['Dividends'][0:index]))
        inflation    = int(((nowCpi+dividendsCpi)/firstCpi)*100)
    return int(((now+dividends)/first)*100) - inflation

def MakePercent(ticker, cpi):
    percent = []
    for i in range(len(ticker.history)):
        percent.append(CalcPercent(ticker, cpi, i))
    return percent

def MakeTicker(name, cpi=None):
    ticker         = Object()
    ticker.name    = name
    ticker.ticker  = yf.Ticker(name)
    # Date, Open, High, Low, Open, Close, Adj Close, Volume, Dividends, Stock Splits
    print('Getting Ticker: ' + name)
    ticker.history = ticker.ticker.history(period="8y", interval="1d")
    # Percentage of every (close + dividends) / starting close
    ticker.percent = MakePercent(ticker, cpi)
    return ticker

def PlotTickers(title, tickers):
    for i in range(len(tickers)):
        for j in range(len(tickers)-1):
            if tickers[j].percent[-1] < tickers[j+1].percent[-1]:
                tickers[j], tickers[j+1] = tickers[j+1], tickers[j]

    maxLabel = 0
    for t in tickers:
        if len(t.name) > maxLabel:
            maxLabel = len(t.name)

    plt.rcParams['font.family'] = 'monospace'            
    for t in tickers:
        x = np.array(t.history.index)
        y = np.array(t.percent)
        plt.plot(x, y, label=t.name.ljust(maxLabel) + ' - ' + format(t.percent[-1])+'%')
        print(t.name.ljust(maxLabel), format(t.percent[-1])+'%')

    leg = plt.legend(loc='upper left')
    plt.grid()
    plt.title(title)
    plt.show()

# List Maker Then Plot
def ListPlot(title, inputList, cpi):
    tmp = []
    for t in list(dict.fromkeys(inputList)):
        tmp.append(MakeTicker(t, cpi))
    PlotTickers(title, tmp)

# Inflation Data
cpi = MakeTicker('CPI')

# Funds
ListPlot('List 1', ['VTI', 'VGT', 'VIG', 'SCHD'], cpi)
ListPlot('List 2', ['VUG', 'DGRO'], cpi)
ListPlot('List 3', ['FXAIX', 'FRLPX'], cpi)
ListPlot('List 4', ['VFIAX', 'VTIVX', 'FFIDX', 'VTI', 'QQQ'], cpi)
