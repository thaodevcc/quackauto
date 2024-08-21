import requests
import time
from colorama import Fore, Back,Style
import threading
# URL để gửi yêu cầu
url = "https://egg-api.hivehubs.app/api/scene/info"
urlcollet = "https://egg-api.hivehubs.app/api/scene/egg/reward"
urltotal = "https://egg-api.hivehubs.app/api/user/assets"

# Headers
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Host": "egg-api.hivehubs.app",
    "Origin": "https://app-coop.rovex.io",
    "Referer": "https://app-coop.rovex.io/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
}

# Payload JSON bao gồm token
payload = {
    "token": "a2fe1118499b4cb7be5298e506b88397"
}

while True:
    # Lấy số lượng trứng tổng
    restotal = requests.post(urltotal, headers=headers, json=payload)
    restotals = restotal.json()
    print(f"Số lượng trứng tổng: {restotals.get('data', {}).get('egg', {}).get('amount', 'N/A')}")

    # Gửi yêu cầu POST với payload
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    res = response.json()
    try:
        if 'data' in res and isinstance(res['data'], list):
            for item in res['data']:
                if 'eggs' in item and isinstance(item['eggs'], list):
                    for egg in item['eggs']:
                        test = egg.get('uid')
                        
                        if test:
                            print(Fore.BLACK+"id", test)
                            rescollet = requests.post(urlcollet, headers=headers, json={"egg_uid": test, "token": payload["token"]})
                            rescollet_data = rescollet.json()
                            print(Fore.RED + f"trứng: {rescollet_data.get('data', {}).get('assets', {}).get('egg', {}).get('amount', 'N/A')}")
                            print(Fore.RED + f"usdt: {rescollet_data.get('data', {}).get('assets', {}).get('usdt', {}).get('amount', 'N/A')}")
                            time.sleep(5)
                        else:
                            print("Không tìm thấy UID trứng, bỏ qua...")
                            time.sleep(6)
                else:
                    print("loading....")
                    time.sleep(80)
                    print(Fore.GREEN+"loading....")
        else:
            print("API Error:")
    
    except requests.RequestException as e:
        print("Requesrs Error:", str(e))

