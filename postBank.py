import json
from pathlib import Path
import pandas as pd

class PostBank:

    def display_post_details(self):
        all_post_details = []
        directory = "posts_profiles"
        
        files = Path(directory).glob('*')
        for file in files:
            with open(file) as data_file:    
                data = json.load(data_file)
                print(data)
                for key in data:

                    post_details = []
                    site_name = data[key]["website_name"]
                    post_category = data[key]["category"]
                    keyword_file = data[key]["keyword_file"]
                    num_of_keywords = ""

                    try:
                        with open (f"keywords_files/{data[key]['keyword_file']}") as k_file:
                            file_data = json.load(k_file)
                    except json.decoder.JSONDecodeError:
                        pass
                    except FileNotFoundError:
                        return 0
                    else:
                        num_of_keywords = len(file_data["keywords"])


                    post_details.extend((site_name, post_category, num_of_keywords))
                    all_post_details.append(post_details)
        return all_post_details


                
                
                

        