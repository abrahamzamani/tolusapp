import requests
import base64
from jinja2 import Environment, FileSystemLoader
import random
import json
from webprofile import WebProfile


class PostCreator:

    def __init__(self, website_name):
        self.details = WebProfile()
        self.login_details = self.details.getProfile(website_name)
        self.wordpress_user = self.login_details["wp_user_name"]
        self. wordpress_pass = self.login_details["app_password"]
        self.api_url = self.login_details["website_url"] +"/wp-json/wp/v2/posts"

        self.wordpress_credentials = self.wordpress_user + ":" + self.wordpress_pass
        self. token = base64.b64encode(self.wordpress_credentials.encode())
        self.header = {'Authorization' : 'Basic ' + self.token.decode('utf-8')}
      
        


    def create_posts(self, post_data, category, keyword):
        k = keyword

        modifiers = ['Most Asked Questions Simplified', f'Others Answers Relating to {k}', 'With Other Related Questions', 'Summary']
        modifier = random.choice(modifiers)
        title = post_data[0]['question']
        file_loader = FileSystemLoader('blogtemplates')
        env = Environment(loader=file_loader)
        post_template = env.get_template('post_template.html')
        post_content = post_template.render(post_data=post_data, modifier=modifier, title=title)

        data = {
        'title':f'{title}: [{modifier}]',
        'status':'publish',
        'slug':title,
        'content': post_content,
        'category': category
                    }

        response = requests.post(self.api_url, headers=self.header,json=data)
        print(response.content)
        
        print(post_content)

    
    def get_categories (website_name):

        with open("webProfiles.json", "r") as profiles:
            data = json.load(profiles)

        link = data[website_name]["website_url"]

        data = requests.get(f"{link}/wp-json/wp/v2/categories")
        json_data = (data.json())

        categories = []
        for element in json_data:
            category = element['name']
            categories.append(category)
        return categories