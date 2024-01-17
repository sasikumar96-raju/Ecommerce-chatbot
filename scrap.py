from bs4 import BeautifulSoup
import csv

with open('index3_monitors.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

result_items = soup.find_all('div', class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")

with open('data.csv', 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Title', 'Rating', 'Price']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for item in result_items:
        title_span = item.find('span', class_="a-size-medium a-color-base a-text-normal")
        title = title_span.text if title_span else ''

        rating_span = item.find('span', class_='a-icon-alt')
        rating = rating_span.text if rating_span else ''

        price_span = item.find('span', class_='a-price-whole')
        price = price_span.text if price_span else ''

        writer.writerow({'Title': title, 'Rating': rating, 'Price': price})

print('Written to data.csv')