import sqlite3
from flask import *


app = Flask(__name__)
app.secret_key = b"ozge"

def findCategories():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    # get the category name
    c.execute("SELECT cname FROM Category")
    check = c.fetchall()
    # Creating category names list
    categoryNames = []
    for cname in check:
        categoryNames.append(cname[0])
    return categoryNames

@app.route("/")
def homePage():
    currentCatagories = findCategories()
    currentCatagories.append("All Categories")
    # if username is added on session display another home page
    # we are checking the user session in the html
    return render_template("index.html", categories=currentCatagories)

@app.post("/loginForm")
def login():
    usernameInput = request.form["usernameInput"]
    passwordInput = request.form["passwordInput"]

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT username,password FROM User WHERE  username = ? and password = ?",(usernameInput,passwordInput))
    check = c.fetchone()
    conn.close()
    # if username and password is match added into session and redirected to homepage
    # and redirected to the homepage, otherwise error message displayed
    if check is not None:
        session["username"] = usernameInput
        return redirect(url_for("homePage"))
    else:
        currentCatagories = findCategories()
        currentCatagories.append("All Categories")
        return render_template("index.html", error="error", categories=currentCatagories)


@app.route("/register")
def register():
    return render_template("register.html")


@app.post("/checkRegister")
def checkRegister():
    username = request.form["register_username"]
    password = request.form["register_password"]
    fullname = request.form["register_fullname"]
    email = request.form["register_email"]
    telephone = request.form["register_telephone"]

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT username FROM User WHERE username = ?",(username,))
    check = c.fetchone()
    # username check if there is no record for that username it passes and adds to database
    # we are checking the password with javascript therefore we do not need to check it again
    # otherwise it shows error message and the user not added to database
    if check is not None:
        # There is a user with this ID.
        return render_template("register.html", registerIsSuccess="false")
    else:
        # if the username is valid adds the user into the database
        c.execute("INSERT INTO User(username,fullname,email,password,telno) VALUES(?, ?,?,?,?)",
                  (username,fullname,email,password,telephone)
                  )
        conn.commit()
        conn.close()
        return render_template("register.html", registerIsSuccess="true")


@app.route("/home")
def returnHome():
    return redirect(url_for("homePage"))

@app.route("/logout")
def logout():
    # current user is deleted in session
    session.pop("username",None)
    # redirect the user to a home page
    return redirect(url_for("homePage"))


@app.route("/showAdvertisementPage")
def showAdveritsementPage():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    # get the previous advertisements
    c.execute("SELECT title,description, User.username,Advertisement.aid, Advertisement.isactive,Category.cname "
              "FROM Advertisement "
              "INNER JOIN  User on User.username=Advertisement.username "
              "INNER JOIN  Category ON Category.cid = Advertisement.cid "
              "WHERE User.username = ?", (session["username"],))

    userAdvertisements = c.fetchall()
    conn.close()
    # previous records and categories added in html to show it
    return render_template("advertisements.html", categories=findCategories(), userAdvertisements=userAdvertisements)


@app.post("/addAdvertisement")
def addAdvertisements():
    title = request.form["title"]
    description = request.form["description"]
    category = request.form['category']

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    c.execute("SELECT cid FROM Category WHERE  cname = ?",(category,))
    category_id = c.fetchone()[0] # tuple that's why [0]

    # advertisement created according to given (title, description, isactive, username, cid)
    c.execute("INSERT INTO Advertisement(title,description,isactive,username,cid) values (?,?,?,?,?)", (title, description, 1, session["username"], category_id))
    conn.commit()
    conn.close()
    # redirected to advertisements
    return redirect(url_for("showAdveritsementPage"))


@app.route("/seeMoreDetails/<string:adId>")
def seeMore(adId):

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    c.execute("SELECT Advertisement.title, Advertisement.description, Category.cname, User.fullname, User.email, User.telno "
              "FROM User "
              "INNER JOIN  Advertisement on User.username=Advertisement.username "
              "INNER JOIN Category on Advertisement.cid = Category.cid "
              "WHERE Advertisement.aid = ?", (int(adId),))

    userAdvertisements = c.fetchall()

    return  render_template("showMore.html",userAdvertisements = userAdvertisements)
    


@app.route("/changeActivateStatus/<int:adId>/<int:status>")
def changeActiveDeactiveStatues(adId, status):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    # when activation button is clicked to change the activation status
    # made it a get request that aid appended and also activation status
    # we changed the activation status
    newStatus = 0 if status == 1 else 1
    # update the activation status according to given aid
    c.execute("UPDATE Advertisement  SET isactive = ? WHERE aid = ?",(newStatus,adId))

    conn.commit()
    conn.close()

    return redirect(url_for("showAdveritsementPage"))


@app.post("/search")
def search():
    # keyword and category_name
    text = request.form["text"]
    selected_Category = request.form["category"]

    currentCatagories = findCategories()
    currentCatagories.append("All Categories")

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    # All categories selected, it searches the all available advertisements which is active
    # Also, it searches in the database then fetches
    if selected_Category == "All Categories":
        c.execute("SELECT title,description, User.fullname,Category.cname,Advertisement.aid FROM Advertisement "
                  "INNER JOIN User on User.username = Advertisement.username "
                  "INNER JOIN Category ON Category.cid = Advertisement.cid "
                  "WHERE isactive=1 and (title LIKE ? OR description LIKE ? OR User.username LIKE ?) ", (f"%{text}%",f"%{text}%",f"%{text}%")
                  )

        values = c.fetchall()

        # Created dictionary to keep track each category advertisements
        categoryAndItsAdvertisements = {}
        for value in values:
            # if it does not exist we create a list for that key, otherwise do not create
            if value[3] not in categoryAndItsAdvertisements:
                categoryAndItsAdvertisements[value[3]] = []
            # temp list for advertisement values
            tempList = []
            tempList.append(value[0])
            tempList.append(value[1])
            tempList.append(value[2])
            tempList.append(value[4])
            # advertisement is added to corresponded category
            categoryAndItsAdvertisements[value[3]].append(tempList)
        # to identify in html, we also send the all category flag
        return render_template("index.html", searchResult=categoryAndItsAdvertisements,categories=currentCatagories, all_selected=True)

    else:
        # Same logic applies the only difference is that now we also check the selected category
        c.execute("SELECT title,description, User.fullname,Category.cname, Advertisement.aid FROM Advertisement "
                  "INNER JOIN User on User.username = Advertisement.username "
                  "INNER JOIN Category on Category.cid =Advertisement.cid "
                  "WHERE isactive=1 and Category.cname = ? and (title LIKE ? or description LIKE ? or User.username LIKE ?) "
                  , (selected_Category,f"%{text}%",f"%{text}%",f"%{text}%"))

        values = c.fetchall()

    if values is not None:
        categoryAndItsAdvertisements = {}
        for value in values:
            if value[3] not in categoryAndItsAdvertisements:
                categoryAndItsAdvertisements[value[3]] = []

    for value in values:
        tempList = []
        tempList.append(value[0])
        tempList.append(value[1])
        tempList.append(value[2])
        tempList.append(value[4])
        categoryAndItsAdvertisements[value[3]].append(tempList)

        return render_template("index.html", searchResult=categoryAndItsAdvertisements, categories=currentCatagories)
    else:
        return render_template("index.html", searchResult="empty",categories=currentCatagories)


@app.route("/profile")
def my_profile():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    # current user fetched in database to show details
    username = session["username"]
    c.execute("SELECT * FROM User WHERE username=?",(username,))
    user_data = c.fetchone()
    # user_data is a user details as tuple
    return render_template("myprofile.html",user_data=user_data)

@app.route("/edit_profile")
def edit_profile():
    # same logic applied but this time to understand the editing added 1 to html
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    username = session["username"]
    c.execute("SELECT * FROM User WHERE username=?", (username,))
    user_data = c.fetchone()

    return render_template("myprofile.html",user_data=user_data, edit=1)

@app.post("/save_changes")
def save_changes():
    # changed details are posted
    password = request.form["password"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    telno = request.form["telno"]
    current_user = session["username"]

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    # updating the user details
    c.execute("UPDATE User SET fullname = ?, email = ?, password = ?, telno = ? WHERE username = ?",
              (fullname, email, password, telno, current_user))

    conn.commit()  # Commit the changes to the database
    conn.close()
    return redirect(url_for('my_profile'))


@app.get("/showhint")
def showHint():
    word = request.args.get('input', None)
    if word is not None:
        conn = sqlite3.connect("shop.db")
        c = conn.cursor()
        c.execute("SELECT title FROM Advertisement "
                  "INNER JOIN User on User.username = Advertisement.username "
                  "INNER JOIN Category ON Category.cid = Advertisement.cid "
                  "WHERE isactive=1 and title LIKE ?  ", (f"{word}%",)
                  )

        values = c.fetchall()

        words = ", ".join([value[0] for value in values])
        return words
    else:
        return ""

if __name__ == "__main__":
    app.run(debug=True)