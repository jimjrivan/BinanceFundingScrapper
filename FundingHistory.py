import re
from datetime import datetime
from math import floor
import time
import requests as req
import pyuser_agent
import traceback
import pandas as pd
from pathlib import Path

header = {
    'user-agent': pyuser_agent.UA().random
}

url_funding_history = "https://www.binance.com/fapi/v1/marketKlines?interval=1m&limit=1000&symbol=pETHUSDT"


def get_funding_history():
    res = req.get(url_funding_history, headers=header)
    #print_request(res)
    return res.json()


def main():
    try:
        listOfFundings = []
        for funding in get_funding_history():
            regexPremiumIndex = re.search("-?\d+\.\d{0,4}", (float(funding[1])*100).__str__(), re.IGNORECASE)
            premiumIndex = regexPremiumIndex.group(0).strip() if regexPremiumIndex else ''
            listOfFundings.append({
                "Time": datetime.fromtimestamp(funding[0]//1000).__str__(),
                "Premium Index": "{0}%".format(premiumIndex)
            })
        listOfFundings.reverse()

        outputExcel(listOfFundings)
    except Exception as e:
        showError(e)


def outputExcel(listOfFundings):
    df = pd.json_normalize(listOfFundings)
    pathExcel = f"./exported_files"
    Path(pathExcel).mkdir(parents=True, exist_ok=True)
    pathExcel += f"/BinanceFundingHistory_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df.to_excel(pathExcel, sheet_name='ETHUSDT Perpetual Premium Index', index=False)


def my_format(num, x):
    return str(num*100)[:4 + (x-1)] + '%'


def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return f'{floor(val) / 10 ** digits}%)'


def print_request(r):
    print(f"URL: {r.url}")
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


def showError(e):
    print(f'Error: {e}')
    print(traceback.format_exc())

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))