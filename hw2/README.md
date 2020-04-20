## FinTech Estimation of stocks
NTU FinTech Introduction Homework, 2019 fall  
Design trading strategies such that the total return of 4 stocks over a given period of time can be maximized.

# DataSet
4 stocks:
* SPY: SPDR S&P 500 ETF Trust (SPY)
* IAU: iShares Gold Trust (IAU)
* LQD: iShares iBoxx $ Investment Grade Corporate Bond ETF (LQD)
* DSI: iShares MSCI KLD 400 Social ETF (DSI)

# Requirements
* python
* numpy
* pandas

# Process
1. Find the best parameter of different use "FindBestParam_<strategy name>.py"
2. Combine method & param implemented in "myStrategy.py"
3. "profitEstimate.py" will execute the function written in "myStrategy.py"

# Execution
```
python profitEstimate.py <stockName.csv>
```




