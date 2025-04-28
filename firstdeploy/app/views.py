from django.shortcuts import redirect, render
from .models import *
import bcrypt

# Create your views here.
def index(request):
    if 'userid' in request.session and request.session['userid']!='':
        return redirect('/dashboard')
    return render(request,"index.html")

def register(request):

    errors=User.objects.validateregistry(postdata=request.POST)
    if len(errors)>0:
        return redirect('/',errors)
    # validate input
    password= request.POST['password']
    pw_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    email=request.POST['email']
    User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)
    return redirect("/")


def login(request):
    user=User.objects.filter(email=request.POST['email'])
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), logged_user.password.encode('utf-8')):
            request.session['userid']=logged_user.id
            return redirect('/dashboard')
    redirect('/')



def dashboard(request):
    userid=request.session['userid']
    context={
        'user':User.objects.get(id=userid),
        'projects':Project.objects.all()
    }
    return render(request,'dashboard.html',context)

def createproject(request):
    userid=request.session['userid']
    context={
        'user':User.objects.get(id=userid)
    }
    return render(request,"createproject.html",context)

def addproject(request):
    errors=Project.objects.validateproject(postdata=request.POST)
    if len(errors)>0:
        return redirect('/createproject',errors)
    
    name=request.POST['name']
    owner=User.objects.get(id=request.session['userid'])
    description=request.POST['description']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']

    Project.objects.create(name=name,owner=owner,description=description,start_date=start_date,end_date=end_date)
    return redirect(f'/project/{Project.objects.last().id}/details')

def details(request,id):
    userid=request.session['userid']
    context={
        'user':User.objects.get(id=userid),
        'project':Project.objects.get(id=id),
        'members':Project.objects.get(id=id).members.all()
    }
    return render(request,"projectdetails.html",context)
        

def updateproject(request,id):
    errors=Project.objects.validateproject(postdata=request.POST)
    if len(errors)>0:
        return redirect(f'/editproject/{id}',errors)
    
    project=Project.objects.get(id=id)
    project.name=request.POST['name']
    project.description=request.POST['description']
    project.start_date=request.POST['start_date']
    project.end_date=request.POST['end_date']
    project.save()

    return redirect(f'/project/{project.id}/details')

def editproject(request,id):
    userid=request.session['userid']
    context={
        'user':User.objects.get(id=userid),
        'project':Project.objects.get(id=id)
    }
    return render(request,"editproject.html",context)

def deleteproject(request,projectid):

    project=Project.objects.get(id=projectid)
    project.delete()
    return redirect('/dashboard')

def join(request,projectid,userid):
    project=Project.objects.get(id=projectid)
    project.members.add(User.objects.get(id=userid))
    print(project.members.all())
    project.save()
    return redirect('/dashboard')

def leave(request,projectid,userid):
    project=Project.objects.get(id=projectid)
    project.members.remove(User.objects.get(id=userid))
    project.save()
    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')