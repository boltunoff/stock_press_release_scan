#TODO       Listen for Sean's lessons: Creating a Watchlist, Press releases to refine requiremetns below
Resources:
Using free version API from
https://intrinio.com/account        # <= 1000 requests a day
API docs:
http://docs.intrinio.com/#securities-search-screener150


User: 5e92761f9c9fc9d23468a554e22d4463
Pass: 08d95c32f7c5293645505d9b0bb978d0

Stock press release URLs:
    Press Releases (Headlines)
1. https://api.intrinio.com/press_releases?ticker=AKER      # up to 10 tickers in one request separated by comma
    Press Releases Content (has keywords)
2. https://api.intrinio.com/press_releases/detail?id=88356
3. Company news!!!:
http://docs.intrinio.com/#company-news
https://api.intrinio.com/news?identifier=HMNY

Yahoo Press Releases:
https://finance.yahoo.com/quote/AAPL/press-releases?p=AAPL

All Stocks Tickers list:
http://docs.intrinio.com/master/us-securities#home

Flow:
============
1. Read Ticker List of ALL ? stocks to find from yahoo or any other free api.
Or just use lowfloat.com list of stocks only?:
Filter  by:
   a. price:                  yahoo, nasdaq?
   b. volume and avg_volume:  yahoo ?
   c. float:                  http://lowfloat.com/all/  <= 10 MM? or so

2. For filtered list in #1 get press releases, create a file for possible Elastic search
    a. id with headlines
    b. content with keywords
    c. get keywords from Sean
    
3. https://finviz.com/news.ashx
4. https://finviz.com/ (Top Gainers, New Highs)
5. https://finviz.com/groups.ashx   (Industry groups)

#TODO       Listen for Sean's lessons: Creating a Watchlist, Press releases to refine requiremetns below
