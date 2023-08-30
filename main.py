import os
import json
import random
import time
# from PIL import Image
import requests
from io import BytesIO
from urllib.request import urlopen
import argparse
import argcomplete
import xlsxwriter
# from bs4 import BeautifulSoup


def get_cardnames(path):
    file = open(path, "r")
    filestr = file.read().split("\n")
    print(filestr)
    return filestr


def create_search_str(cardname_list):
    print(cardname_list)
    # cardname_list = ["Akroan Horse", "Omnath, Locus of the roil", "Elsha of the Infinite"]

    # str_a = "https://api.scryfall.com/cards/search?q="
    str_b = "&unique=cards&as=grid&order=name"

    str_c = "https://api.scryfall.com/cards/search?q=%28" + cardname_list[0].replace(" ", "+").replace(",", "%2C") + "%29"
    for c_card in cardname_list[1:19]:
        str_i = "%28" + c_card.replace(" ", "+").replace(",", "%2C") + "%29"
        str_c = str_c + "+or+" + str_i
    str_c = str_c + str_b

    print(str_c)
    return str_c


def url2str(url):
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")


def get_card_pool(search_str):  # PULL DATA FROM SEARCH LINK
    printing = True

    html_string = url2str(search_str)
    # print(html_string)
    cards = []
    has_more = True
    if printing: print("get_card_pool: loop opened")
    while has_more:
        jver = json.loads(html_string)
        cards += jver["data"]
        if printing: print("get_card_pool:", len(cards), "/", jver["total_cards"])
        if jver["has_more"]:
            if printing: print("get_card_pool: has more...")
            html_string = url2str(jver["next_page"])
            # cards += json.loads(url2str(jver["next_page"]))["data"]
        else:
            has_more = False
            if printing: print("get_card_pool: loop closed")
    # print(cards)
    return cards


def save_to_xlsx(chosen_cards, result_path):
    workbook = xlsxwriter.Workbook(result_path)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Card Name")
    worksheet.write(0, 1, "USD")
    worksheet.write(0, 2, "NZD")
    price_list = []
    for i, c_card in enumerate(chosen_cards):
        print(i, c_card['name'])
        print(c_card['prices']['usd'] != None)
        if (c_card['prices']['usd'] != None):
            worksheet.write(i+1, 0, c_card['name'])
            c_card_price = c_card['prices']['usd']
            worksheet.write(i+1, 1, float(c_card_price))
            worksheet.write(i+1, 2, float(c_card_price) * 1.55)
            price_list.append(float(c_card_price) * 1.55)
    print(price_list)
    workbook.close()


def main(options):
    # cardname_list = get_cardnames(options.input_path)
    # print(cardname_list)
    # search_str = create_search_str(cardname_list)
    search_str = "https://api.scryfall.com/cards/search?q=set%3Ajmp&unique=cards&as=grid&order=name"
    cards = get_card_pool(search_str)
    # print(cards)
    save_to_xlsx(cards, options.result_path)

# input: player name, rand num, images/json or both
# output: card names, linked, time/date rolled, player name,

# search string
# loop through all cards
# get list of qualities
# perform function?

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ScuffleGen")
    parser.add_argument('-ip', '--input_path', default="card_list.txt")
    parser.add_argument('-rp', '--result_path', default="results_collated.xlsx", type=str)

    argcomplete.autocomplete(parser)

    main(parser.parse_args())
