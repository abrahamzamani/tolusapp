import json

class WebProfile:

    

    def createProfile (self, website_name, wp_user_name, website_url, app_password):

        new_profile = {
            website_name:{
                "website_url":website_url,
                "wp_user_name":wp_user_name,
                "app_password":app_password
            }
        }

        try:
            with open("webProfiles.json", "r") as profiles:
                #read the file as a python dictionary
                data = json.load(profiles)
        except FileNotFoundError:
            # if the file was not found then create a new file
            with open("webProfiles.json", "w") as profiles:
                json.dump(new_profile, profiles, indent=4)
        else:
            # updating the python dictionary with the new profile entry
           data.update(new_profile)

           # after updating the data as a python dictionary, turning back to a json file.
           with open("webProfiles.json", "w") as profiles:
            #saving updated data in json json
            json.dump(data, profiles, indent=4)

    def getProfile(self, website_name):
        with open("webProfiles.json", "r") as profiles:
            data = json.load(profiles)

            profile = data[website_name]
        return profile 


    def getProfile_name(self):
        profile_name = []

        with open("webProfiles.json", "r") as profiles:
            data = json.load(profiles)

            profile_name = list(data.keys())
        return profile_name

    