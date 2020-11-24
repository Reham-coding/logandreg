from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request,'index.html')
def success(request):
        # login status check
    if request.session["login_user"]["status"]:
        this_user = User.objects.get(id=request.session["login_user"]["login_id"])

        context = {
            "first_name" : this_user.firstname,
            "last_name" : this_user.lastname,
        }
        return render(request, "success.html", context)
    
    else:
        messages.error(request, "Login error", extra_tags = "login_error")
        redirect("/")

    return render(request,'success.html',context )


def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST["pass"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(firstname = request.POST['firstname'], lastname =request.POST['lastname'], email = request.POST['email'], password  = pw_hash)
        request.session["login_user"] = { "status": True, "login_id": User.objects.get(email=request.POST["email"]).id }
      
        return redirect("/success")

def log(request):
    
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session["login_user"] = { "status" : True, "login_id" : User.objects.get(email=request.POST["email"]).id }
        return redirect("/success")

def logout(request):
    del request.session["login_user"]
    return redirect("/")

    
    

  
  
