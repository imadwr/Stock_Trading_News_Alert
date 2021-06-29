import requests
import smtplib
import os


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.getenv("stock_apikey")
NEWS_API_KEY = os.getenv("news_apikey")

user_email = os.getenv("email")
user_password = os.getenv("password")
to_email = os.getenv("to_email")


# stock price
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_data = response.json()["Time Series (Daily)"]
print(stock_data)

days_list = [value for (key, value) in stock_data.items()]

prev_day_close_price = float(days_list[0]["4. close"])
prev_prev_day_close_price = float(days_list[1]["4. close"])

difference = abs(prev_day_close_price - prev_prev_day_close_price)
print(difference)
price_percentage = (difference/prev_day_close_price) * 100
print(price_percentage)

if price_percentage > 5:
    print("Get news")
# get news
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()
    news_data_list = news_data["articles"]

    articles_list = [{"title": item["title"], "description": item["description"]} for item in news_data_list][:3]
    formatted_articles = [f"Subject: {article['title']}\n\n{article['description']}" for article in articles_list]
    print(formatted_articles)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user_email, password=user_password)

        for article in formatted_articles:
            connection.sendmail(
                from_addr=user_email,
                to_addrs=to_email,
                msg=article
            )
