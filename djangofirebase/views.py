
import pyrebase 
from django.shortcuts import render 


config = {

    "apiKey": "AIzaSyA0mrCBrXado1rzKvX4BZPd1XhFXclFdR0",
    "authDomain": "django-firebase-736df.firebaseapp.com",
    "databaseURL": "https://django-firebase-736df.firebaseio.com",
    "projectId": "django-firebase-736df",
    "storageBucket": "django-firebase-736df.appspot.com",
    "messagingSenderId": "749084881521",

    "appId": "1:749084881521:web:e939e0ea3684f896fc61d0",
    "measurementId": "G-EK9015KGKR"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def signIn(request):
    return render(request, "signIn.html")

def postSign(request):

    #authentification
    email = request.POST.get("email")
    passw = request.POST.get("pass")

    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        msg = "invalid credantials"
        return render(request,"signIn.html",{"msg":msg})

    # saving user to session
    request.session["sess_user"] = user

    # retrieve messages from Firebase
    messages = getFirebaseMessages()

    return render(request, "welcome.html", {"e":user["email"],"m":messages})


def postMessage(request):
    data = {
        "message": request.POST.get("message")
    }

    # retrieve user from session
    user = request.session["sess_user"]

    # refresh token
    auth.refresh(user['refreshToken'])

    # Pass the user's idToken to the push method
    results = db.child("messages").push(data, user["idToken"])

    # retrieve messages from Firebase
    messages = getFirebaseMessages()

    return render(request, "welcome.html", {"e":user["email"],"m":messages})



def getFirebaseMessages():
    """
    Because Pyrebase generate a list of objects, and each
    object must be called with .val(), we can not pass it directly
    to the views (because the functions no more exists).
    So we must build a simple list of values...
    """
    list_messages = {}
    messages = db.child("messages").get()

    for m in messages.each():
        list_messages[m.key()] = m.val()["message"]

    return list_messages