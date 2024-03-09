
from django.shortcuts import render, get_object_or_404, redirect
# render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import UserForm, DiffForm, StudentForm, RoomForm,SignUpForm
from .models import Diff, Student, Room, Change, Swap, Hostel
from .binary_tree import HostelBinaryTree, sorted_hostels
from django.contrib.auth.models import User
from django.template import RequestContext
import csv, os
from .pbinary import HostelPricingBinaryTree, sorted_pricing
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from .custom_auth import custom_authenticate
# Diff class for authentication if login user is not hostel admin or Student then
# login page will display error 
# @login_required

def get_hostel_details(request):
    hostel_name = request.GET.get('name', None)
    hostel = Hostel.objects.filter(name=hostel_name).first()
    image_urls = [image.image.url for image in hostel.images.all()]
    try:
        hostel = Hostel.objects.filter(name=hostel_name).first()
        if hostel:
            hostel_details = {
            'name': hostel.name,
            'location': hostel.address,
            'contact':hostel.contact,
            'available_rooms': (hostel.seater2+ hostel.seater3),
            'seater2': hostel.seater2,
            'seater3':hostel.seater3,
            'images':[{'url': url} for url in image_urls]

            # Add other fields as needed
            }
        else:
            hostel_details = {'error': 'Hostel not found'}
    except Exception as e:
        hostel_details = {'error': str(e)}


    return JsonResponse(hostel_details)


def sort_by_hostels(request):  
    context = {'context': sorted_hostels}
    return render(request, 'hostel/sorted_hostels.html', context)

def sort_by_pricing(request):
    
    context = {'context': sorted_pricing}
    return render(request, 'hostel/sorted_hostels.html', context)


def indexx(request):
    # diff = Diff.objects.get( user = request.user)
    # return render(request, 'hostel/index.html', {'diff' : diff, })
    return render(request,'hostel/indexx.html')

# def signin(request):
#     return render(request,'hostel/signin.html')
# def signup(request):
#     return render(request,'hostel/signup.html')


# --------- RegisterPage view --------
# @login_required
def register(request):
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form    = UserForm(request.POST)
        diff_form    = DiffForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        
            
        if user_form.is_valid() and diff_form.is_valid() and student_form.is_valid():
            try:
                user = user_form.save()
                # user.username(label_tag='roll_no')
                # using set_password method, hash the password
                user.is_active = False
                user.set_password(user.password)
                user.save()
                
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                diff = diff_form.save(commit = False)
                diff.user = user
                diff.save()
                student  = student_form.save(commit = False)
                student.roll_no = user
                student.save()
                registered = True
                
                return HttpResponseRedirect('/')
            except:
                pass

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        student_form = StudentForm()
        diff_form = DiffForm()

    return render(request,'hostel/register.html', {
        'user_form' : user_form,
        'student_form' : student_form,
        'diff_form' : diff_form,
        'registered': registered,
    })

def signin(request):
    # try:
    #     diff = Diff.objects.get(user=request.user)
    # except Diff.DoesNotExist:
    #     diff = Diff.objects.create(user=request.user)
    
    hostels = Hostel.objects.all()
    

    

    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        auth_result = custom_authenticate(username, password)

        if isinstance(auth_result, User):
            # Authentication successful
            login(request, auth_result)
            return render(request, "hostel/index.html",  {'hostels': hostels})
        elif auth_result == "username_not_found":
            messages.error(request, "Username not found")
        elif auth_result == "incorrect_password":
            messages.error(request, "Incorrect password")
        return render(request, "hostel/signin.html")
        # user = authenticate( username=username, password=password)
        # print(user)
        # if user is not None:
        #     login(request,user)
            
        #     return render(request,"hostel/index.html")

        # else:
        #     messages.error(request,"Bad Credentials!")
        #     print("bad credentials")
        #     return render(request,"hostel/signin.html")

    return render(request,"hostel/signin.html", {'hostels': hostels})

    #     if user:
    #         if user.is_active:
    #             # We'll send the user back to the homepage.
    #             login(request, user)

    #             return HttpResponseRedirect('/index')
    #         else:
    #             return HttpResponse('Your Account is disabled')
    #     else:
    #         print ("Invalid login details: {0}, {1}".format(username, password))
    #         messages.add_message(request, messages.ERROR, 'Invalid Password or Username. Try again!')
    #         return HttpResponseRedirect("/signin")
    # else:
    #     return render(request,'hostel/signin.html', {})
# --------- Login --------
# @login_required
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate( username=username, password=password)

        if user:
            if user.is_active:
                # We'll send the user back to the homepage.
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your Account is disabled')
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            messages.add_message(request, messages.ERROR, 'Invalid Password or Username. Try again!')
            return HttpResponseRedirect("/login")
    else:
        return render(request,'hostel/login.html', {})



def view_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    return render(request, 'hostel/view_hostel.html', {'hostel': hostel})

@login_required
def index(request):
    try:
        diff = Diff.objects.get(user=request.user)
    except Diff.DoesNotExist:
        diff = Diff.objects.create(user=request.user)
    
    hostels = Hostel.objects.all()
    

    return render(request, 'hostel/index.html', {'diff': diff, 'hostels': hostels})




# <!----- Logout----->
@login_required
def logout1(request):
    logout(request)
    return redirect('/login/')

# <!-------Allocate Room ------>
@login_required
def allocate(request):

    if request.method == 'POST':

        roll_no = request.POST['roll_no']
        room_no = request.POST['room_no']

        try:
            student_roll_no = User.objects.get(username = roll_no)
            student = Student.objects.get(roll_no = student_roll_no)
            room_new = Room.objects.get(room_no = room_no)
            
            
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the details again!')
            return render(request, 'hostel/staff_allocate_room.html', {})
        
        if room_new is not None and student.room is None:
            if room_new.vacancy > 0:
                student.room = room_new
                room_new.vacancy -= 1
                student.save()
                room_new.save()
                return HttpResponseRedirect('/')
            else:
                html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Sorry, The Room is full</h2> </body></html>'
                return HttpResponse(html)
        else:
            return HttpResponseRedirect('/')
    
    else:
        return render(request, 'hostel/staff_allocate_room.html', {})


@login_required
def student_details(request):
    student = Student.objects.get(roll_no = request.user)
    room = Room.objects.get(room_no = student.room.room_no)
    students  = Student.objects.filter(room = student.room.room_no)
    return render(request, 'hostel/student_details.html', {'student': student,'room1': room,'students':students })


@login_required
def change_request(request):

    if request.method == 'POST':
        student = Student.objects.get(roll_no = request.user)
        reason  = request.POST['reason']
        flag    = request.POST['flag']

        if flag:
            request = Change.objects.create(student = student, reason = reason)
        else:
            return HttpResponseRedirect('/')
        
        return HttpResponseRedirect('/success')
    else:
        return render(request, 'hostel/change_req.html', {})
        

@login_required
def change(request):
    if request.method == 'POST':
        roll_no  = request.POST['roll_no']
        room_no  = request.POST['room_no']

        try:
            user = User.objects.get(username = roll_no)
            student = Student.objects.get(roll_no = user)
            room_new = Room.objects.get(room_no = room_no)
       
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the details again!')
            return render(request, 'hostel/staff_change_room.html', {})
        
        if room_new is not None and student.room is not None:
            if room_new.vacancy > 0:
                old_room = Room.objects.get(room_no = student.room.room_no)
                old_room.vacancy += 1
                student.room = room_new
                room_new.vacancy -= 1
                old_room.save()
                student.save()
                room_new.save()
                return HttpResponseRedirect('/')
            else:
                html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Sorry, The Room is full</h2> </body></html>'
                return HttpResponse(html)
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/staff_change_room.html', {})

@login_required
def swap_request(request):
    if request.method == 'POST':

        stud2 = request.POST['stud2']
        reason   = request.POST['reason']
        flag     = request.POST['flag']

        try:
            user = User.objects.get(username = stud2)
            student2  = Student.objects.get( roll_no = user)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Check the roll number again!')
            return render(request, 'hostel/swap_request.html', {})

        student1 = Student.objects.get(roll_no = request.user)
        if student2.room is not None:
            if flag:
                Swap.objects.create(student1 = student1, student2 = student2, reason = reason)
            else:
                return HttpResponseRedirect('/')
            return HttpResponseRedirect('/success')
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/swap_request.html', {})

@login_required
def swap(request):

    if request.method == 'POST':

        roll_no1 = request.POST['roll_no1']
        roll_no2 = request.POST['roll_no2']

        try:
            user1 = User.objects.get(username = roll_no1)
            student1 = Student.objects.get(roll_no = user1)
            user2 = User.objects.get(username = roll_no2)
            student2 = Student.objects.get(roll_no = user2)

        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'check the details again!')
            return HttpResponseRedirect('hostel/staff_swap_room.html', {})
        
        if student1.room is not None and student2.room is not None:

            room1 = student1.room
            room2 = student2.room
            student1.room = room2
            student2.room = room1
            student1.save()
            student2.save()
            html = '<html><body style="background-color:rgb(123,225,236); text-align:center; margin-top:100px;"><h2>Room Swapped Successfully</h2> </body></html>'
            return HttpResponse(html)
        
        else:
            return HttpResponseRedirect('/')
    
    else:
        return render(request, 'hostel/staff_swap_room.html', {})

@login_required
def swap_ack(request):

    user = request.user
    try:
        req = Swap.objects.get(student2 = request.user.username)
    except Swap.DoesNotExist:
        req = None
    if request.method == 'POST':

        if '_accept' in request.POST:
            req.accept = True
            req.save()
        if '_decline' in request.POST:
            req.delete()
        return HttpResponseRedirect('/success')
    else:
        return render(request, 'hostel/swap_ack.html', {'request': req, 'user': user})


@login_required
def deallocate(request):
    if request.method == 'POST':
        join_year = request.POST['join_year']

        students = Student.objects.filter(join_year = join_year)
        length = len(students)
        if length == 0:
            messages.add_message(request, messages.ERROR, 'No Such Batch')
            return render(request, 'hostel/deallocate.html', {})
        
        else:
            for i in range(length):
                if students[i].room is not None:
                    old_room = Room.objects.get(room_no = students[i].room.room_no)
                    old_room.vacancy = old_room.capacity
                    print (students[i], old_room)
                    old_room.save()
                    students[i].room = None
                    students[i].save()
                    print (students[i],old_room)
                else:
                    students[i].save()
            return HttpResponseRedirect('/')
    else:
        return render(request, 'hostel/deallocate.html', {})

@login_required
def show_request(request):
    try:
        swap_req = Swap.objects.all()
    except Swap.DoesNotExist:
        swap_req = None

    try:
        changer = []
        change_req = Change.objects.all()
        for i in change_req:
            user = User.objects.get(username=i.student.roll_no)
            changer.append([user, i])
            #print (user, i)

    except Change.DoesNotExist:
        change_req = None
    return render(request, 'hostel/show_request.html', {'swap_req': swap_req, 'change_req': changer})

@login_required
def vacant_room(request):
    rooms = Room.objects.exclude(vacancy = 0)
    return render(request, 'hostel/vacant_room.html', {'rooms': rooms,})

@login_required
def show_students(request):
    changer = []
    students = Student.objects.all()
    for i in students:
        user = User.objects.get(username = i.roll_no)
        changer.append([user, i])
    
    return render(request, 'hostel/show_students.html', {'students': changer,})


@login_required
def success(request):
    return render(request, 'hostel/success.html', {})


# def signup(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         email=request.POST['email']
#         password=request.POST['password']

#         if User.objects.filter(username=username):
#             messages.error(request,"username already exists")
#             return redirect('127.0.0.1:8000/signup/')

#         if User.objects.filter(email=email):
#             messages.error(request,"email already exists")
#             return redirect('indexx')
        
#         myuser=User.objects.create_user(username,email,password)

#         myuser.is_active=False
#         myuser.save()

#         messages.success(request,"your accocunt is successfully created")

#         # return render(request,"hostel/signup.html/")
#         # return redirect('127.0.0.1:8000/signup/')
#         return render(request,'hostel/signup.html')

#     return render(request,"hostel/signup.html/")


def signup(request):
    registered = False

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        # print("hi")

        if signup_form.is_valid():
            try:
                username = signup_form.cleaned_data['username']
                email = signup_form.cleaned_data['email']
                password = signup_form.cleaned_data['password']

                user = User.objects.create_user(username, email, password)
                user.is_active = False
                user.save()

                registered = True

                # return HttpResponseRedirect('/indexx')
                return render(request,'hostel/index.html')
                
            except Exception as e:
                print ("Invalid login details: {0}, {1}".format(username, password))
                # Handle exceptions if any (e.g., username or email already exists)
                pass

    else:
        signup_form = SignUpForm()

    return render(request, 'hostel/signup.html', {
        'signup_form': signup_form,
        'registered': registered,
    })
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .hostel_trie import hostel_trie  # Adjust this import based on your actual model
from .hostel_trie import HostelTrie
@csrf_exempt  # Disable CSRF for simplicity (handle CSRF properly in production)
def search_hostel(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        
        search_results = hostel_trie.search(search_query)
        print(search_results)

        # Retrieve detailed information about the hostels
        hostels = Hostel.objects.filter(name__in=search_results)

        # Serialize the data to JSON
        
        data = []
        for hostel in hostels:
            image_urls = [image.image.url for image in hostel.images.all()]

            hostel_data = {
                'name': hostel.name,
                'address': hostel.address,
                'pricing': hostel.pricing,
                'images': [{'url': url} for url in image_urls]
            }
            data.append(hostel_data)

        return JsonResponse({'search_results': data})
    return HttpResponse(status=400)
