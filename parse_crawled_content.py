import os
import re
import requests 
from thefuzz import fuzz
import pickle
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import shutil
import time

def get_by_id(paper_id):
    
    session = requests.Session()
    retries = Retry(total=2, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        # Make the API call using the session
        response = requests.post(
            'https://api.semanticscholar.org/graph/v1/paper/batch',
            params={'fields': 'title,abstract,tldr,year,embedding'},
            json={"ids": [paper_id]})
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        if response.status_code == 200:
            return response
        else:
            return None
    except requests.exceptions.RequestException as e:
        # Handle exceptions or log the error
        print(f"Error: {e}")
        return None


def get_id(title,orig_name):
    api_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title}
    
    response = requests.get(api_url, params=params)
    print(f":::::: CAPTURED TITLE: {title}")
    if response.status_code == 200:
        
        result = response.json()
        if result['total'] >= 1:
            print(f":::::: Found Semantic Scholar record(s)")
            for re in result['data']:
                #print(fuzz.partial_ratio(re['title'].lower(),title.lower()))
                if fuzz.partial_ratio(re['title'].lower(),title.lower()) >= 90:
                    print(f":::::: Found paper ID for {title} at 90% partial fuzzy match.")
                    return re['paperId']
        print(f"!!!!! SKIPPING Please check {orig_name}")
        return None
    else:
        return None

# Directory path containing text files
directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"crawler","crawler_output")

regex_title_patterns = [
    re.compile(r'entitled “(.*?)”'),
    re.compile(r'entitled["“](.*?)["”]'),
    re.compile(r'entitled: “(.*?)”.'),
    re.compile(r'entitled“(.*?)”'),
    re.compile(r'paper: “(.*?)”'),
    re.compile(r'paper “(.*?)”'),
]

text_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

if not os.path.exists(os.path.join(directory_path, 'collection')):
    os.makedirs(os.path.join(directory_path, 'collection'))

if not os.path.exists(os.path.join(directory_path, 'processed')):
    os.makedirs(os.path.join(directory_path, 'processed'))

for file_name in text_files:
    file_path = os.path.join(directory_path, file_name)
    file_processed_path = os.path.join(directory_path, 'processed', file_name)

    # Read the content of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove mrmh contributor names
    content = re.sub(r'By Mathieu Boudreau', '', content)
    content = re.sub(r'By Pinar S. Ozbay', '', content)
    content = re.sub(r'By Agah Karakuzu', '', content)
    
    # Iterate over multiple regex patterns
    for regex_pattern in regex_title_patterns:
        match = regex_pattern.search(content)
        if match:
            extracted_text = match.group(1)
            paper_id = get_id(extracted_text,file_name)
            time.sleep(1)
            if paper_id:
                results = get_by_id(paper_id)
                time.sleep(1)
                results = results.json()
                print(f"----------- GOT RESULTS: {results[0]['title']}")
                new_file_name = f"{paper_id}.txt"
                if results[0]['tldr']:
                    content = f"Title: {results[0]['title']} \nAbstract: {results[0]['abstract']} \nTLDR: {results[0]['tldr']['text']} \nReproducibility Insights:\n{content}"
                else:
                    content = f"Title: {results[0]['title']} \nAbstract: {results[0]['abstract']} \nReproducibility Insights:\n{content}"
            else:
                # Skip if cannot process.
                break
                # content = f"Title: {extracted_text} \nReproducibility Insights:\n{content}"

            new_file_path = os.path.join(directory_path, 'collection', new_file_name)
            print(f'--------------------------------/n WRITING: {new_file_path}')
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f'--------------------------------/n MOVING: {file_processed_path}')
            shutil.move(file_path,file_processed_path)
            # One go is enough
            break

