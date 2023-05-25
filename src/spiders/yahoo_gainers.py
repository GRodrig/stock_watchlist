import aiohttp
from scrapy.selector import Selector
from schemas import StockType, YahooGainLoser

URL_GAINERS = 'https://finance.yahoo.com/{}/'


async def get_gainer_loser(type: StockType, offset: int=0, count: int=100):
    """
    Get gainers/losers from Yahoo Finance
    :param offset:
    :param count:
    :return:
    """
    name = 'yahoo_gainers'

    params = {
        'offset': offset,
        'count': count
    }
    headers = { 
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'DNT'             : '1', # Do Not Track Request Header 
        'Connection'      : 'close'
    }

    cookies = {
        'B': '7t389hlgv4sqv&b=3&s=gb',
        'GUCS': 'AU8-5cgT',
        'EuConsent': 'CPTv0BMPTv0BMAOACBENB-CoAP_AAH_AACiQIJNe_X__bX9n-_59__t0eY1f9_r3v-QzjhfNt-8F2L_W_L0H_2E7NB36pq4KuR4ku3bBIQFtHMnUTUmxaolVrzHsak2MpyNKJ7LkmnsZe2dYGHtPn9lD-YKZ7_7___f73z___9_-39z3_9f___d9_-__-vjfV_993________9nd____BBIAkw1LyALsSxwJNo0qhRAjCsJCoBQAUUAwtEVgAwOCnZWAT6ghYAITUBGBECDEFGDAIAAAIAkIiAkALBAIgCIBAACAFCAhAARMAgsALAwCAAUA0LEAKAAQJCDI4KjlMCAiRaKCWysQSgr2NMIAyywAoFEZFQgIlCCBYGQkLBzHAEgJYAYaADAAEEEhEAGAAIIJCoAMAAQQSA',
        'A1': 'd=AQABBF9z8mECELBiwNCF9soE8MMAyI0JjX4FEgABBgHX-mHJYvbPb2UB9iMAAAcIX3PyYY0JjX4&S=AQAAAjnkhOf_LxrMMNCN1-BYfEY',
        'A3': 'd=AQABBF9z8mECELBiwNCF9soE8MMAyI0JjX4FEgABBgHX-mHJYvbPb2UB9iMAAAcIX3PyYY0JjX4&S=AQAAAjnkhOf_LxrMMNCN1-BYfEY',
        'A1S': 'd=AQABBF9z8mECELBiwNCF9soE8MMAyI0JjX4FEgABBgHX-mHJYvbPb2UB9iMAAAcIX3PyYY0JjX4&S=AQAAAjnkhOf_LxrMMNCN1-BYfEY&j=GDPR',
        'GUC': 'AQABBgFh-tdiyUIdFwSP',
        'cmp': 'v=22&t=1643742832&j=1',
    }

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0),trust_env=True, headers=headers, cookies=cookies) as session:
        async with session.get(URL_GAINERS.format(type.value), params=params) as response:
            if response.status != 200:
                return handle_error(name, response.status, response.url)
            
            response = Selector(text=(await response.text()))
            stocks_info = response.xpath('//tbody/tr')
            stocks = [YahooGainLoser(
                symbol=stock.xpath('.//td[1]//text()').get(),
                name=stock.xpath('.//td[2]//text()').get(),
                price=stock.xpath('.//td[3]//text()').get(),
                change=stock.xpath('.//td[4]//text()').get(),
                percent_change=stock.xpath('.//td[5]//text()').get(),
                volume=stock.xpath('.//td[6]//text()').get(),
                avg_volume=stock.xpath('.//td[7]//text()').get(),
                market_cap=stock.xpath('.//td[8]//text()').get(),
                pe_ratio=stock.xpath('.//td[9]//text()').get(),
            ) for stock in stocks_info]
            return {"spider": name, type.value: stocks}
        


def handle_error(name, status, url=None):
    error = "Spider error"
    if status >= 500:
        error = "Scraper crashed - Connection problem with {}".format(url)
    return {"spider": name, "error": error, "status": status}


