from flask import Flask, redirect, render_template, request, session, url_for   
from webprofile import WebProfile
from wpPostCreator import PostCreator
from controlApp import Control
from extractSheetData import ExtractSheetData
from postBank import PostBank


app = Flask(__name__)
app.config['SECRET_KEY'] = 'unwe8fo238fuq0fij2309iqd09'

@app.route("/", methods=["GET","POST"])
def index():
    list_counter = 0
    pb = PostBank()
    get_post_details = pb.display_post_details()

    if get_post_details == 0:
        return render_template("index.html", get_post_details=get_post_details, list_counter=list_counter)


   

    if request.method == "POST":
        website_name = request.form["website_name"]
        category = request.form["category"]
        num_of_post = request.form["post_num"]
        print("......................")
        print(website_name)
        print(category)
        print(num_of_post)
        print("......................")

        start_creating_post = Control()
        start_creating_post.createPost(website_name, category, num_of_post)

    return render_template("index.html", get_post_details=get_post_details, list_counter=list_counter)

@app.route("/createprofile", methods=["GET","POST"])
def create_new_profile():


    if request.method == "POST":
        website_name = request.form["website_name"]
        wp_user_name = request.form["wp_user_name"]
        website_link = request.form["website_link"]
        app_password = request.form["application_password"]
    
        if not website_name or not wp_user_name or not website_link or not app_password:
            return "failure"

        profile = WebProfile()
        profile.createProfile(website_name, wp_user_name, website_link, app_password)
    return render_template("createProfile.html")



@app.route("/addkeywords", methods=["GET","POST"])
def add_keywords():
    post_categories = ""

    profile = WebProfile()
    website_names = profile.getProfile_name()

    if request.method == "POST":

        try:
            session["site"] = request.form["website"]
        except:
            link = request.form["link"]
            category = request.form["category"]
            sheet_Data = ExtractSheetData(link)
            get_keywords = sheet_Data.extract_keywords()
            save_or_update_keywords = sheet_Data.save_keywords(session["site"], category, get_keywords)
            print(get_keywords)

        else:

            post_categories = PostCreator.get_categories(session["site"])
            redirect(url_for("add_keywords"))

        return render_template("addkeywords2.html", categories=post_categories)

    return render_template("addkeywords.html", website_names=website_names)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)