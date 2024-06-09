import requests
import os
from dotenv import load_dotenv
from pandas import DataFrame


load_dotenv()


def get_currency() -> str:
    url = "https://developerhub.alfabank.by:8273/partner/1.0.1/public/nationalRates?currencyCode=840,978,643"
    request = requests.get(url)
    data = request.json()
    rates = data.get("rates")

    currencies = {
        "Date": rates[0].get("date"),
        "Currency ISO": [rate.get("iso") for rate in rates],
        "Currency Rate": [rate.get("rate") for rate in rates],
    }
    df = DataFrame(data=currencies)

    return df.to_string(index=False, header=False)


def send_notification(msg: str) -> None:
    token = os.getenv("BOT_TOKEN")
    group_id = os.getenv("GROUP_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": group_id,
        "text": msg,
    }
    req = requests.post(url, params=params)
    req.raise_for_status()


if __name__ == "__main__":
    message = get_currency()
    send_notification(message)
