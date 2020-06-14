from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Profile,Appointments
# Create your views here.


def index(request):
    return render(request,"index.html",{})

@login_required(login_url='/admin/login')
def patients(request):
    patients = Profile.objects.filter(role="patient")
    return render(request,"patients.html",{"patients":patients})

@login_required(login_url='/admin/login')
def doctors(request):
    doctors = Profile.objects.filter(role="doctor")
    return render(request,"doctors.html",{"doctors":doctors})

@login_required(login_url='/admin/login')
def nurses(request):
    nurses = Profile.objects.filter(role="nurse")
    return render(request,"nurses.html",{"nurses":nurses})

@login_required(login_url='/admin/login')
def technicians(request):
    technicians = Profile.objects.filter(role="technician")
    return render(request,"technicians.html",{"technicians":technicians})

@login_required(login_url='/admin/login')
def appointment(request):
    appointments = Appointments.objects.all()
    return render(request,"appointment.html",{"appointments":appointments})

@login_required(login_url='/admin/login')
def search_results(request):
    if 'user' in request.GET or request.GET['user']:
        search_item = request.GET.get('user')
        searched_users = Profile.objects.filter(email=search_item)
        return render(request, 'search.html',{"users": searched_users})
    else:
        return redirect("/")

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,email=email, password=raw_password)
            profile = Profile(user=user)
            profile.save()
            user.is_active = True
            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'sign.html', {'form': form})



# @login_required(login_url='/auth/login')
# def profile(request):
#     jobs = Jobs.objects.filter(user = request.user)
#     if request.method == 'POST':
#         jobsForm = JobsForm(request.POST,request.FILES)
#         profForm = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
#         if profForm.is_valid():
#             profForm.save()
#             return redirect('profile')
#         if jobsForm.is_valid():
#             job = jobsForm.save(commit=False)
#             job.driver = request.user
#             job.user = request.user
#             job.save()
#             return redirect('profile')
#     profForm = ProfileForm()
#     jobsForm = JobsForm()
#     return render(request,'profile/profile.html',{"prof":profForm,"jobform":jobsForm,"jobs":jobs})
        
# @login_required(login_url='/auth/login')
# def pickjob(request,pk):
#     jobb = Jobs.objects.get(id=pk)
#     pickedjob = PickedJobs(driver=request.user,job=jobb)
#     jobb.picked = "true"
#     jobb.save()
#     pickedjob.save()
#     return redirect('profile')

# @login_required(login_url='/auth/login')
# def finishJob(request,pk):
#     jobb = Jobs.objects.get(id=pk)
#     pickedjob = PickedJobs.objects.get(job=jobb)
#     jobb.delivered = "true"
#     pickedjob.completed = "true"
#     jobb.save()
#     pickedjob.save()
#     return redirect('profile')


    
# @login_required(login_url='/auth/login')
# def search_results(request):
    
#     if 'user' in request.GET or request.GET['user']:
#         search_item = request.GET.get('user')
#         searched_users = User.objects.filter(username=search_item)
#         message = f"{search_item}"
#         return render(request, 'profile/search.html',{"message":message,"users": searched_users})
#     else:
#         message = "You haven't searched for any user"
#         return render(request, 'profiles.html',{"message":message})

# @login_required(login_url='/auth/login')
# def profiles(request,pk):
#     profile = Profile.objects.get(user_id=pk)
#     jobs = Jobs.objects.filter(user=profile.user)
#     return render(request,"profile/profiles.html",{"profile":profile,"jobs":jobs})