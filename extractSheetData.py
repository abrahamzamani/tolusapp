import keyword
from urllib.parse import urlparse
import pandas as pd 
import json
from pathlib import Path
import os

class ExtractSheetData:

    def __init__(self, url):
        self.url = urlparse(url)
        self.parsed_url = f"{self.url.scheme}://{self.url.netloc}{self.url.path[:-4]}export?format=csv"
    

    def extract_keywords (self):
        
        sheet_data = pd.read_csv(self.parsed_url)
        keyword_data = sheet_data
        
        return keyword_data


    def save_keywords(self, website_name, category, keyword_data):

        keywords_column_name = []
        new_data = keyword_data

        for col in new_data.columns:
            keywords_column_name.append(col)
        print("-----------------------------")

        new_keywords = new_data[keywords_column_name[0]].to_list()
       
        #********************************************************************************#
        filepath = Path(f'keywords_files/{category}_keywords.json')

        store_keywords = {
            "keywords":[]
        }
        

        try:
            with open(filepath, "r")as f:
                #read the file as a python dictionary
                data = json.load(f)

        except FileNotFoundError:
            for i in new_keywords:
                store_keywords["keywords"].append(i)
            print(store_keywords)
            with open(filepath, "w") as f:
                json.dump(store_keywords, f, indent=4)
            file_name = os.path.basename(filepath)
            self.posts_profiles(website_name, category, file_name)
            print("created")

        else:
            for k in new_keywords:
               data["keywords"].append(k)
            print(data)
            
            file_name = os.path.basename(filepath)
            self.posts_profiles(website_name, category, file_name)
           
            # after updating the data as a python dictionary, turning back to a json file.
            with open(filepath, "w") as f:
                #saving updated data in json json
                json.dump(data, f, indent=4)
                print("updated")


        print("")
        print("")
        print("")
        print("")
        print("")
        
    def posts_profiles(self, website_name, category, keyword_file):
        new_profile = {
            f"{website_name}_{category}": {
                    "website_name": website_name,
                    "category":category,
                    "keyword_file":keyword_file
            }
        }

        filepath = Path(f"posts_profiles/{website_name}_posts.json")

        try:
            with open(filepath, "r") as profiles:
                data = json.load(profiles)
        except FileNotFoundError:
            with open(filepath, "w") as profiles:
                json.dump(new_profile, profiles, indent=4)
        else:
            data.update(new_profile)

            with open(filepath, "w") as profiles:
                json.dump(data, profiles, indent=4)


        

        

   