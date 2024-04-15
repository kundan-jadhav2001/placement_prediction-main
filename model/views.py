from django.shortcuts import render
from .models import user, predicted, review
from random import randint
import smtplib
from django.core.mail import send_mail

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def test(request):
    return render(request, "prediction/test.html")

# Create your views here.
def home(request):
    return render(request, "index1.html")

def signinup(request):
    try:
        value = request.COOKIES['Signin']
        return render(request, 'prediction/predictionpage.html')
    except:
        return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def blog(request):
    return render(request, "blog.html")

def course(request):
    return render(request, "course.html")

def savereview(request):
    if request.method == "POST":
        Review = review(Name = request.POST["name"], Email = request.POST["Email"],Opinions = request.POST["Opinions"])
        Review.save()
        
    return render(request, "prediction/review.html", {"data":review.objects.all()})

def logout(request):
    try:
        response = render(request, "index1.html")
        response.delete_cookie("Signin")
        return response
    except:
        return render(request, "index1.html")

def confirmsignup(request):
    msg = "" 
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email'].lower()
        password = request.POST['password']
        
        try: 
            user.objects.get(Email=email)
            msg = "Email is already taken. Use another or Login using same email"
            
        except Exception as e:
            if str(e) == "user matching query does not exist.":
                usr = user(Name=name, Email=email,Password=password) # create new model instance
                usr.save() #seve to db
                msg = "Registration completed. Please signin to continue."
            else:
                msg = str(e)
    return render(request, "index.html", {"msg":msg})

        
    

def confirmsignin(request):
    msg = ''
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password'] 

        try: 
            usr = user.objects.get(Email=email)
            if usr.Email==email and usr.Password==password:
                response = render(request, "prediction/predictionpage.html", {"msg":msg})
                response.set_cookie('Signin', email ,max_age=1*24*60*60)
                return response
            else:
                return render(request, 'index.html', {'msg':"Email and password don't match"})
            
        except Exception as e:
            if str(e) == "user matching query does not exist.":
                msg = "This email is not registered. Please Signup first."
            else:
                msg = str(e)
    return render(request, 'index.html',{'msg':msg})

def predictionpage(request):
    try:
        value = request.COOKIES['Signin']
        return render(request, 'prediction/predictionpage.html')
    except KeyError:
        return render(request, 'index.html', {'msg':"Please Signin to check the predictions."})


def predict(request):
    import joblib,os
    import numpy as np
    from django.conf import settings
    from sklearn.preprocessing import MinMaxScaler
    import warnings
    warnings.simplefilter("ignore")
    
    if request.method == "POST":
        Age = int(request.POST["Age"])
        Gender = int(request.POST["Gender"])
        Stream = int(request.POST["Stream"])
        NumOfInternships = int(request.POST["Internships"])
        CGPA = float(request.POST["CGPA"])
        Backlogs = int(request.POST["Backlogs"])
        WebDevlopment = int(request.POST["webdevelopment"])
        DataScience = int(request.POST["datascience"])
        GameDevlopment = int(request.POST["gamedevelopment"])
        AndroidDevlopment = int(request.POST["androiddevelopment"])
        GraphicsDesigner = int(request.POST["graphicsdesigner"])

        with open(os.path.join(settings.BASE_DIR, 'model/model_campus_placement.pkl'),'rb') as f:
            model = joblib.load(f)
            pred = model.predict([[Age,Gender,Stream,NumOfInternships,CGPA,Backlogs,WebDevlopment,DataScience,GameDevlopment,AndroidDevlopment,GraphicsDesigner]])[0]

        if pred==1:
            try:
                email = request.COOKIES['Signin']
                name = user.objects.get(Email=email).Name
            except KeyError:
                return render(request, 'index.html', {'msg':"Please Signin to check the predictions."})
            predicted(
                Name=name,
                Email=email,
                Age=Age,
                Gender= "Male" if Gender==1 else"Female",
                Stream= "Electronics and Communication" if Stream==0 else "Computer Science" if Stream==1 else "Information Technology" if Stream==2 else "Mechanical" if Stream==3 else "Electrical" if Stream==4 else "Civil",
                NumberOfInternships=NumOfInternships,
                CGPA=CGPA,
                Backlogs=Backlogs,
                WebDevlopment= WebDevlopment,
                DataScience= DataScience,
                GameDevlopment=GameDevlopment,
                AndroidDevlopment=AndroidDevlopment,
                GraphicsDesigner=GraphicsDesigner,
                Prediction= "High Chances" if pred==1 else "Low Chances"
                ).save()
            beginner = []
            if WebDevlopment==0:
                beginner.append("WebDevelopment")
            if DataScience==0:
                beginner.append("DataScience")
            if GameDevlopment==0:
                beginner.append("GameDevelopment")
            if AndroidDevlopment==0:
                beginner.append("AndroidDevelopment")
            if GraphicsDesigner==0:
                beginner.append("GraphicsDesigner")
            print(beginner)
            return render(request, 'prediction/result.html', {'prediction':pred,'beginner':beginner})
        if pred==0:
            try:
                email = request.COOKIES['Signin']
                name = user.objects.get(Email=email).Name
            except KeyError:
                return render(request, 'index.html', {'msg':"Please Signin to check the predictions."})
            predicted(
                Name=name,
                Email=email,
                Age=Age,
                Gender= "Male" if Gender==1 else"Female",
                Stream= "Electronics and Communication" if Stream==0 else "Computer Science" if Stream==1 else "Information Technology" if Stream==2 else "Mechanical" if Stream==3 else "Electrical" if Stream==4 else "Civil",
                NumberOfInternships=NumOfInternships,
                CGPA=CGPA,
                Backlogs=Backlogs,
                WebDevlopment= WebDevlopment,
                DataScience= DataScience,
                GameDevlopment=GameDevlopment,
                AndroidDevlopment=AndroidDevlopment,
                GraphicsDesigner=GraphicsDesigner,
                Prediction= "High Chances" if pred==1 else "Low Chances"
                ).save()
            beginner = []
            if WebDevlopment==0:
                beginner.append("WebDevelopment")
            if DataScience==0:
                beginner.append("DataScience")
            if GameDevlopment==0:
                beginner.append("GameDevelopment")
            if AndroidDevlopment==0:
                beginner.append("AndroidDevelopment")
            if GraphicsDesigner==0:
                beginner.append("GraphicsDesigner")
            return render(request, 'prediction/result.html', {'beginner':beginner, "len":len(beginner)})
    else:   
        return render(request, 'prediction/result.html', {'prediction':0, "len":len(beginner)})

def report(request):

    try:
        value = request.COOKIES['Signin']
        data = predicted.objects.filter(Email=value)
        print("report" ,data)
    except KeyError:
        return render(request, 'index.html', {'msg':"Please Signin to check the predictions."})
    except Exception as e:
        print(e)
        return render(request, 'prediction/database.html', {'msg':"No data to show"})
    return render(request, 'prediction/database.html', {'data':data})

def front(request):
    return render(request, 'prediction/front.html')

def feedback(request):
    return render(request, 'feedback.html')

def enterotp(request):
    return render(request, "forgotpass.html")

def forgotpass(request):
    if request.method == 'POST':
        global otp,email
        try:
            entered_otp = request.POST['otp']
            print("otp:",otp)
            if int(entered_otp) == int(otp):
                return render(request, 'newpass.html')
            else:
                return render(request, 'forgotpass.html', {'msg':"OTP didn't matched", 'otp':''})
        except:
            otp = randint(100000, 999999)
            body = f'The OTP for password reset is {otp}'
            
            
            try:
                email = request.POST["email"]
                print(email)
                row = user.objects.get(Email=email)
            except Exception as e:
                print(e)
                return render(request, 'forgotpass.html',{'msg':"Error while connecting to database", 'otp':''})

            if row != None:
                try:
                    my_email = "en20133485@git-india.edu.in"
                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.login(my_email, "xyz@8910")

                    message = MIMEText(f"Your otp is {otp}")
                    message["From"] = my_email
                    message["To"] = email
                    message["Subject"] = "Forgot passward OTP"
                    
                    server.sendmail(my_email, email, message.as_string())
                    print("Email sent successfully!")


                    print("otp sent ", otp)
                    return(render(request, "forgotpass.html",{'otp':otp, "email":request.POST['email']}))
                except Exception as e:
                    print(e)
            else:
                return render(request, 'forgotpass.html',{'msg':"Email not found in database. You don't have accound", 'otp':''})
    return(render(request, "forgotpass.html" ))
    

def setnewpass(request):
    global email
    print(email)
    if request.method == "POST":
        newpass = request.POST['pass1']
        confnewpass = request.POST['pass2']
        usr = user.objects.get(Email=email)
        usr.Password = newpass
        usr.save()
        return render(request, 'index.html', {'msg':'Password changed. Login with new password'})
    return render(request, 'forgotpass.html')

