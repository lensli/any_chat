import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
st = '''写一段复杂的python程序
这是一个复杂的Python程序，它是一个简单的Web爬虫，用于从网站上抓取信息。



import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    for article in soup.find_all('article'):
        row = {}
        try:
            row['headline'] = article.h2.a.text
        except AttributeError:
            row['headline'] = None
        try:
            row['summary'] = article.find('div', {'class': 'entry-content'}).p.text
        except AttributeError:
            row['summary'] = None
        try:
            row['date'] = article.time['datetime']
        except TypeError:
            row['date'] = None
        rows.append(row)
    return rows

def save_to_csv(rows, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def main():
    url = 'https://www.example.com'
    rows = scrape_website(url)
    save_to_csv(rows, 'output.csv')

if __name__ == "__main__":
    main()
在这个程序中，我们首先定义了一个函数scrape_website，该函数接收一个URL，并使用requests库来获取该URL的HTML内容。然后，我们使用BeautifulSoup库来解析HTML内容，并找到所有的'article'标签。

对于每个'article'标签，我们尝试获取其标题、摘要和发布日期，并将这些信息存储在一个字典中。最后，我们将所有的字典存储在一个列表中，并返回这个列表。

然后，我们定义了一个函数save_to_csv，该函数接收一个列表和一个文件名，然后将列表中的信息写入CSV文件。

最后，我们定义了一个main函数，该函数调用上述两个函数来抓取网站上的信息，并将信息保存到CSV文件中。'''
st = "写一段复杂的python程序"
print(len(enc.encode(st)))

# To get the tokeniser corresponding to a specific model in the OpenAI API:
# enc = tiktoken.encoding_for_model("gpt-4")