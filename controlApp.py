from extractSheetData import ExtractSheetData
from paaScraper import PaaScraper
from paraphraser import Paraphraser
from wpPostCreator import PostCreator
import json
from pathlib import Path
import pandas as pd


class Control:

    def createPost(self, website_name, category, num_of_post):

        getwebsite = website_name
        getcategory = category
        number_of_post = num_of_post
        profile_filepath = Path(f"posts_profiles/{website_name}_posts.json")
        print(profile_filepath)
        paraphraser = Paraphraser()
        paraphraser.log_in
       


        with open(profile_filepath, "r") as file:
            post_profile = json.load(file)
            print(post_profile)

            for key in post_profile:
                if key == f"{website_name}_{category}":
                    get_keyword_file = post_profile[key]["keyword_file"]

                    
                    #---------------------------------------------------------------------#
               
                    keyword_filepath = Path(f"keywords_files/{get_keyword_file}")

                    try:
                        with open(keyword_filepath, "r") as file:
                            get_keywords = json.load(file)
                    except FileNotFoundError:
                        pass
                    else:
                        keywords = get_keywords["keywords"]
                        print(keywords)
                       
                        for i in range (int(number_of_post)):
                            print(keywords[i])

                            scrape_paa_data = PaaScraper(keywords[i])
                            paa_data = scrape_paa_data.scraper()
                            scrape_paa_data.quit_driver()
                            
                            print(paa_data)
                            print("...........................................................")
                            print("")
                            print("")
                        # #....................................................

                            for each_data in paa_data:

                                answer = each_data['answer']
                                paraphrased_answer = paraphraser.paraphrased_data(answer)
                                each_data['answer'] = paraphrased_answer

                            post_creator = PostCreator(website_name)
                            post_creator.create_posts(paa_data,getcategory,keywords[i])
                            print(paa_data)
                            keywords.pop(i)
                            
                            with open(keyword_filepath, "w") as f:
                                json.dump(get_keywords, f, indent=4)

                            if keywords == []:
                                print("TRUE")
                                try:

                                    with open(profile_filepath, "r") as file:
                                        post_profile = json.load(file)
                                        print(post_profile)
                                except FileNotFoundError:
                                    pass
                                else:

                                    delete = [key for key in post_profile if key == f"{website_name}_{category}"]
                                    for key in delete:
                                        del post_profile[key]
                                    print(post_profile)
                                    with open(profile_filepath, "w") as file:
                                        json.dump(post_profile, file, indent=4)
                        paraphraser.log_out()


                            

                           
                

