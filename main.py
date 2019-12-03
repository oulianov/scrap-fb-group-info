# -*- coding: ISO-8859-1 -*-
"""Scripts that downloads HTML pages of correctly specified URL in pages.csv into downloads/...
It then extracts relevant data from the downloaded page and store them into output.csv
The pages correspond to facebook group pages, and the relevant data is the number of new posts
today and the number of members."""

import urllib.request
import csv
import time, random
import sys

### Parameters ###

LIST_OF_ADDRESSES = 'pages.csv'
OUTPUT_FILE = 'output.csv'

# If set to True, will always download pages from LIST_OF_ADDRESSES (even if they have already been downloaded)
FORCE_DOWNLOAD = False

# Used for file cleaning. We want addresses starting with this. 
STARTS_WITH = 'https://www.facebook.com/groups/'

### Functions ### 

def csv_to_list(filename, delimiter=";", header=True):
    """Read the csv file (filename) and returns list of its first column's data."""
    with open(filename, 'r') as csvfile:
        data = []
        reader = csv.reader(csvfile, delimiter=delimiter)
        for i, row in enumerate(reader):
            if header: 
                if i>0:
                    # We verify i>0 to avoid reading the header
                    data.append(row[0]) 
            else: 
                data.append(row[0])
    return data


def append_line_to_csv(line, filename, delimiter=";"):
    """Appends a line to the csv file (filename)"""
    text = ""
    with open(filename, 'a+') as csv_file:
        for column in line:
            text = text + str(column) + delimiter
        text = text + "\n"
        csv_file.write(text)


def filter_addresses(addresses, starts_with):
    """Returns addresses that starts with starts_with."""
    filtered_addresses = [a for a in addresses if a[:len(starts_with)] == starts_with]
    return filtered_addresses


def file_exists(file):
    """Returns whether a file exists or not. We check that by trying to open said file."""
    exists = False
    try: 
        with open(file, 'r') as txt:
            exists = True
    except:
        pass
    return exists


def delete_file_content(file_name):
    """Delete the content of a file."""
    try:
        with open(file_name, 'w') as file:
            return True
        return False
    except:
        return False


def download_html_page(address, file_name, wait=(4,8), timeout=15, verbose=False):
    """Downloads the html page at address into file_name; then waits randomly between wait[0] and wait[0]+wait[1].
    If success returns True, if not returns False."""
    # Use a random header to "fool" the website
    if random.random()>0.5:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'fr-FR,fr;q=0.8',
                   'Connection': 'keep-alive'}
    else:
        hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'fr-FR,fr;q=0.8',
                   'Connection': 'keep-alive'}
    # Create a connection to the address
    req = urllib.request.Request(address, headers=hdr)
    with urllib.request.urlopen(req, timeout=timeout) as page:
        with open(file_name, 'w', encoding="utf-8") as output_file:  
            content = page.read().decode('utf-8')
            if verbose: 
                print(content[0:100])
            output_file.write(content)
            # To avoid being flagged as a bot and to overcharge the servers, wait.
            time.sleep(wait[0]+random.random()*wait[1])
            return True
    try:
        pass
    except:
        print(sys.exc_info()[0])
        time.sleep(random.random())
        return False


def scrap_from_html(file_name, verbose=True):
    """Reads a downloaded html pages and returns content that matters in our use case."""
    with open(file_name, "r",  encoding="utf-8") as file:
        content = file.read()
        new_posts, members = None, None
        if len(content)>0: # If file is not empty.
            # Find the number of new posts
            i = content.find('_63om _6qq6')
            c = content[i:i+60]
            new_posts = c[c.find('>')+1:c.find('<')]
            def clean(x):
                # If the number has a comma in it, we need to remove it. 
                x = x.replace('\xa0', '')
                try:
                    x = int(x)
                except:
                    x = None
                return x
            new_posts = clean(new_posts)
            
            # Find the number of members
            i = content.find('_63om _6qq6', i+1)
            c = content[i:i+60]
            members = c[c.find('>')+1:c.find('<')]
            members = members.replace('\xa0', '')
            members = clean(members)
            return members, new_posts

### Script ###

if __name__ == '__main__':
    # Read the addresses
    addresses = csv_to_list(LIST_OF_ADDRESSES)
    addresses = filter_addresses(addresses, STARTS_WITH)

    delete_file_content('errors.txt')
    delete_file_content(OUTPUT_FILE)

    for i, address in enumerate(addresses):
        group_name = address[len(STARTS_WITH):].replace('/', '')
        file_name = "downloads/" + group_name + '.html'
        # If the file does not exists, download it. Note that it might already been downloaded before.
        success = False
        if not file_exists(file_name):
            success = download_html_page(address, file_name)
            if not success:
                # Failed to download the file. Add it to the errors.txt file
                print('Failed to download page : ', address)
                with open('errors.txt', 'a+') as errors_file:
                    errors_file.write(address + '\n')
        if file_exists(file_name) or success:
            print('Processing ', file_name)
            scraped_data = list(scrap_from_html(file_name))
            # Save this scraped data.
            append_line_to_csv([address] + [group_name] + scraped_data, OUTPUT_FILE)

