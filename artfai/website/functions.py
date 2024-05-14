import pandas as pd
import numpy as np
import os
import json
from dotenv import load_dotenv, find_dotenv
import requests

# Harvard Class
'''

class HarvardMuseumAPI:    
    def __init__(self):
        load_dotenv(find_dotenv()) # Loads the environment variables
        self.api_key = os.getenv('HARVARD_API_KEY') # Loads Harvard API Key
        self.base_url = "https://api.harvardartmuseums.org" # Base URL for Harvard API
        self.all_records_info = [] # List to store all records
    
    def pagination(self, url):
        r = requests.get(url)
        # Convert data to jSON format                 
        
        data = r.json()
        # Extract the info and records
        info = data['info']
        records = data['records']
        
        # For each record of objects, print the title and classification
        for record in records:
            record_info = {
                'title': record.get('title', 'Unknown Title'),
                'classification': record.get('classification', 'Unknown Classification'),
                'creditline': record.get('creditline', 'Unknown Creditline'),
                'provenance': record.get('provenance', 'Unknown Provenance'),
                'division': record.get('division', 'Unknown Division'),
                'baseimageurl': record.get('baseimageurl'),
                'iiiifbaseuri': record.get('iiiifbaseuri'),
                'height': record.get('height', 'Unknown Height'),
                'dated': record.get('dated', 'Unknown Date'),
                'medium': record.get('medium', 'Unknown Medium'),
                'imageid': record.get('imageid', 'Unknown Image ID'),
                'technique': record.get('technique', 'Unknown Technique'),
                
                
            }
            
            self.all_records_info.append(record_info)    
            
        try:
            # If there is a next page, repeat pagination function
            if (info['next']):
                self.pagination(info['next'])
        # If next page doesn't work, end function
        except:
            pass
        
        return self.all_records_info
    
    def search_all(self, query):
        url = f"{self.base_url}/object?title={query}&apikey={self.api_key}"
        results  = self.pagination(url)
        
        if results is None:
            print("No results found.")
        
        return results
              
               
    def provenance(self,query, df=None):
        if df is None:
            df = pd.DataFrame()

        url = f"{self.base_url}/object?person={query}&apikey={self.api_key}"
        
        while url:
            r = requests.get(url)
            data = r.json()
            info = data['info']
            records = data['records']

            # Extract relevant data from each record
            record_data = []
            for record in records:
                record_data.append({
                    'title': record['title'],
                    'classification': record['classification'],
                    'century': record['century'],
                    'provenance': record['provenance']
                })

            # Append record data to DataFrame
            df = pd.concat([df, pd.DataFrame(record_data)], ignore_index=True)

            # Get the URL for the next page, if it exists
            url = info.get('next')

        return df



query = "Paul Cezanne"
#query = "dog"
harvard_object = HarvardMuseumAPI()
search = harvard_object.search_all(query)
print(search)
print(len(search))
#result = harvard_object.provenance(query)
#print(result)
#print(len(result))
#print(len(result))
'''


## Victoria and Albert Museum API
class VicAlAPI:
    def __init__(self):
        self.all_records_info = [] # List to store all records
        self.url = "https://api.vam.ac.uk/v2/objects"
       
       
    def search_all(self, query, exact_match=False):
        page = 1
        all_records = []
        if exact_match:
            query = f'"{query}"'
        while True:
            req = requests.get(f'{self.url}/search?q={query}&page={page}')
            object_data = req.json()
            object_records = object_data['records']
            all_records.extend(object_records)
            page += 1
            if page > object_data['info']['pages']:
                break
        
        df = pd.DataFrame(all_records)
        filename = f"{query}_search_results.csv"
        df.to_csv(filename, index=False)
        return df

vicai = VicAlAPI()
query = "Paul Cezanne"
search = vicai.search_all(query, exact_match=True)
print(search)                  

