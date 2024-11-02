import requests
import json
import time
from colorama import Fore, Style

target_usd_market_cap = 30000  # Miinimal mcap
max_target_usd_market_cap = 59000
name_filter = "trump"  # Name filter blank aja klo gak mau filter nama
base_url = "https://frontend-api.pump.fun/coins?offset={}&limit=50&sort=created_timestamp&order=ASC&includeNsfw=false" #ganti ASC jadi DESC untuk terbaru

def fetch_data(offset):
    url = base_url.format(offset)
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "if-none-match": "W/\"ee8d-EmJiZzbCL7vfLv8lJtrxF7ugRE8\"",
        "priority": "u=1, i",
        "referrer-policy": "strict-origin-when-cross-origin",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://pump.fun/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    return response

filtered_items = []
for offset in range(100, 601, 50):
    response = fetch_data(offset)
    print(f"{Fore.YELLOW}Requesting offset: {offset}...{Style.RESET_ALL}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                print(f"{Fore.GREEN}>>>>>>>>> Data found with offset: {offset}{Style.RESET_ALL}")
                for item in data:
                    usd_market_cap = item.get("usd_market_cap", 0)
                    name = item.get("name", "").lower()  
                    if target_usd_market_cap < usd_market_cap <= max_target_usd_market_cap:
                        if name_filter == "" or name_filter.lower() in name:
                            filtered_item = {
                                "mint": item.get("mint"),
                                "name": item.get("name"),
                                "symbol": item.get("symbol"),
                                "twitter": item.get("twitter"),
                                "telegram": item.get("telegram"),
                                "usd_market_cap": usd_market_cap
                            }
                            filtered_items.append(filtered_item)

                print(f"{Fore.CYAN}Total items with usd market cap between {target_usd_market_cap} and {max_target_usd_market_cap}: {len(filtered_items)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No data found at offset: {offset}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Response content is not valid JSON. Content: {response.text}{Style.RESET_ALL}")
            break
    else:
        print(f"{Fore.RED}Failed to fetch data, status code: {response.status_code}, content: {response.text}{Style.RESET_ALL}")
        break
with open('result.json', 'w') as f:
    json.dump(filtered_items, f, indent=4)

print(f"{Fore.GREEN}Filtered items saved to result.json. Total items: {len(filtered_items)}{Style.RESET_ALL}")
