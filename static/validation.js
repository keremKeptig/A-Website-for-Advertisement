
function checkValues()
{
    var title = document.forms["advertisementForm"]["title"].value;
    var description = document.forms["advertisementForm"]["description"].value;
    var category = document.forms["advertisementForm"]["category"].value;

     if(title == "")
    {
        var errorMessage = "title should be entered.";
        document.getElementById("errormessage").innerHTML=errorMessage;
        document.getElementById("errormessage").style.display="block";
        return false;
    }
      if(description == "")
    {
        var errorMessage = "description should be entered.";
        document.getElementById("errormessage").innerHTML=errorMessage;
        document.getElementById("errormessage").style.display="block";
        return false;
    }
       if(category == "")
    {
        var errorMessage = "fullname should be selected.";
        document.getElementById("errormessage").innerHTML=errorMessage;
        document.getElementById("errormessage").style.display="block";
        return false;
    }
}

function checkUserValues(){
    var usernameInput = document.forms["loginform"]["usernameInput"].value;
    var passwordInput = document.forms["loginform"]["passwordInput"].value;


     if(usernameInput == "")
    {
        var errorMessage = "Username should be entered.";
        document.getElementById("errormessage").innerHTML=errorMessage;
        document.getElementById("errormessage").style.display="block";
        return false;
    }
      if(passwordInput == "")
    {
        var errorMessage = "Password should be entered.";
        document.getElementById("errormessage").innerHTML=errorMessage;
        document.getElementById("errormessage").style.display="block";
        return false;
    }

}
function checkUserRegister()
        {
            var username = document.forms["registerForm"]["register_username"].value;
            var password = document.forms["registerForm"]["register_password"].value;
            var fullname = document.forms["registerForm"]["register_fullname"].value;
            var email = document.forms["registerForm"]["register_email"].value;
            var telephone = document.forms["registerForm"]["register_telephone"];

             if(username == "")
            {
                var errorMessage = "Username should be entered.";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }
              if(password == "")
            {
                var errorMessage = "password should be entered.";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }
               if(fullname == "")
            {
                var errorMessage = "fullname should be entered.";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }
                if(email == "")
            {
                var errorMessage = "email should be entered.";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }
                 if(telephone == "")
            {
                var errorMessage = "telephone should be entered.";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }

            var checkPasswordValue = checkPassword(password);
            if(checkPasswordValue == "error")
            {
                var errorMessage = "the password should include at least one\n" +
                        "upper case letter, one lower case letter, one digit and one of these symbols [+, !, *, -] and its length\n" +
                        "should be at least ten. ";
                document.getElementById("errormessage").innerHTML=errorMessage;
                document.getElementById("errormessage").style.display="block";
                return false;
            }

            return true;

        }

function checkPassword(pwd)
{
    if (
        pwd.length < 10 ||
        pwd.search(/[A-Z]/) === -1 ||
        pwd.search(/[a-z]/) === -1 ||
        pwd.search(/\d/) === -1 ||
        pwd.search(/[+!*\-]/) === -1
    )
    {
        return "error";
    }

}
