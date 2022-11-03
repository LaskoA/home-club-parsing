import csv
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://home-club.com.ua/ua/sku-90507603?gclid=CjwKCAjwzY2bBhB6EiwAPpUpZhSieA2DRWXhLcbNCpIvJcC9dLHc534Djx5FKNpL9iXaLZlSQaNyLBoCEwYQAvD_BwE"

results = []


def create_file(data: list):

    with open("home-club.txt", "w", encoding="utf-8", newline="\n") as file:
        first_row = ["артикуль", "наявність для поставки", "Прогноз наявності в Польщі", "Наявність у Львові"]

        writer = csv.writer(file)
        writer.writerow(first_row)
        for item in data:
            writer.writerow([item["артикль"], item["наявність для поставки"],
                             item["Прогноз наявності в Польщі"], item["Наявність у Львові"]])


def get_data():

    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    details = soup.select_one(".additional-details")

    article = details.select_one("div:nth-child(1)").select_one(".value").text
    availability_for_delivery = details.select_one("div:nth-child(2)").select_one(".value").text
    poland_forecast = details.select_one("div:nth-child(3)").select_one(".value").text
    lviv_availability = details.select_one("div:nth-child(5)").select_one(".value").text

    results.append(
        {
            "артикль": article,
            "наявність для поставки": availability_for_delivery,
            "Прогноз наявності в Польщі": poland_forecast,
            "Наявність у Львові": lviv_availability
        }
    )

    create_file(results)


if __name__ == "__main__":
    print("Starting to parse...")
    get_data()
    print("Done")
