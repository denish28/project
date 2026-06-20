from django.shortcuts import render

# Create your views here.
from urllib import request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection
from django.conf import settings
import os

##-----ADMIN WIEWS-----##
# Create your views here.
def adlogin(request):  
    if "username" in request.session:
        return redirect('addashboard') 
    if request.method == 'POST':
        un=request.POST.get('username')
        pw=request.POST.get('password')
        with connection.cursor() as cursor:
            q="select * from adlogin where username=%s and password=%s"
            cursor.execute(q,[un,pw])
            data=cursor.fetchone()
            if data:
                request.session['username']=data[1]
                messages.success(request, 'you are successfully logged in')
                return redirect('addashboard')
            else:
                error='Invalid username or password'
                return render(request, 'admin/adlogin.html', {'error': error})

    return render(request, 'admin/adlogin.html')


def addashboard(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        # counts for dashboard cards
        cursor.execute("select count(*) from adjobs")
        job_count = cursor.fetchone()[0]
        cursor.execute("select count(*) from applied_job")
        app_count = cursor.fetchone()[0]
        cursor.execute("select count(*) from aduser")
        user_count = cursor.fetchone()[0]
        # get job listings for table
        cursor.execute("select * from adjobs")
        data = cursor.fetchall()
        datalist = [
            {
                'id': row[0],
                'category': row[1],
                'position': row[2],
                'company': row[3],
                'address': row[4],
                'contact': row[5],
                'email': row[6],
                'image': row[7],
            }
            for row in data
        ]

    # render dashboard with counts and jobs list
    return render(request,'admin/addashboard.html',
        {
            'jobs': datalist,
            'job_count': job_count,
            'app_count': app_count,
            'user_count': user_count,
        },
    )


def add_jobs(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        if request.method == 'POST':
           cat=request.POST.get('category')
           pn=request.POST.get('position')
           cn=request.POST.get('company')
           ad=request.POST.get('address')
           cnt=request.POST.get('contact')
           em=request.POST.get('email')
           img=request.FILES.get('image')

           image_r_p = None
           if img:
               image_path=os.path.join(settings.MEDIA_ROOT,"jobs", img.name)
               os.makedirs(os.path.dirname(image_path), exist_ok=True)
               with open(image_path, 'wb') as f:
                     for chunk in img.chunks():
                          f.write(chunk)
               image_r_p=settings.MEDIA_URL+"jobs/"+img.name

           q="insert into adjobs(category,position,company,address,contact,email,image) values(%s,%s,%s,%s,%s,%s,%s)"
           cursor.execute(q,[cat,pn,cn,ad,cnt,em,image_r_p])
           messages.success(request, 'Job added successfully.')
           return redirect('manage_jobs')
    return render(request, 'admin/add_jobs.html')


def manage_jobs(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        q="select * from adjobs order by id desc"
        cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],
                'category': row[1],
                'position': row[2],
                'company': row[3],
                'address': row[4],
                'contact': row[5],
                'email': row[6],
                'image': row[7],
            }
            for row in data
        ]
    return render(request, 'admin/manage_jobs.html', {'jobs': datalist})


def delete_data(request, id):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as c:
         q="delete from adjobs where id=%s"
         c.execute(q,[id])
         messages.success(request, 'Job deleted successfully.')
    return redirect('manage_jobs')


def applications(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        q="select * from applied_job"
        cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],
                'name': row[1],
                'category': row[4],                  # added category field
                'company': row[6],
                'position': row[5],                 # added position field  
                'email': row[2],
                'contact': row[3],
                'image': row[7],
            }
            for row in data
        ]
    return render(request, 'admin/applications.html', {'applications': datalist})


def delete_application(request, id):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as c:
        q="delete from applied_job where id=%s"
        c.execute(q,[id])
        messages.success(request, 'Application deleted successfully.')
    return redirect('applications')


def users(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        q="select * from aduser"
        cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'contact': row[3],
                'city': row[4],
                'password': row[5],
                
            }
            for row in data
        ]
    return render(request, 'admin/users.html', {'users': datalist})


def delete_user(request, id):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as c:
        q="delete from aduser where id=%s"
        c.execute(q,[id])
        messages.success(request, 'User deleted successfully.')
    return redirect('users')

def edit_jobs(request, id):
      if not request.session.get('username'):
        return redirect('adlogin')
      with connection.cursor() as cursor:
            q="select * from adjobs where id=%s"
            cursor.execute(q,[id])
            job_data=cursor.fetchone()
            
            if not job_data:
                  return redirect('manage_jobs')
            
            job = {
                  'id': job_data[0],
                  'category': job_data[1],
                  'position': job_data[2],
                  'company': job_data[3],
                  'address': job_data[4],
                  'contact': job_data[5],
                  'email': job_data[6],
                  'image': job_data[7],
            }

            if request.method == "POST":
                  cat=request.POST.get('category')
                  pn=request.POST.get('position')
                  cn=request.POST.get('company')
                  ad=request.POST.get('address')
                  cnt=request.POST.get('contact')
                  em=request.POST.get('email')
                  img=request.FILES.get('image')
                  
                  image_r_p=job['image']
                  if img:
                        image_path=os.path.join(settings.MEDIA_ROOT,"jobs", img.name)
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        with open(image_path, 'wb') as f:
                              for chunk in img.chunks():
                                    f.write(chunk)
                        image_r_p="/myapp/static/images/jobs/"+img.name
                  
                  q="update adjobs set category=%s, position=%s, company=%s, address=%s, contact=%s, email=%s, image=%s where id=%s"
                  cursor.execute(q,[cat,pn,cn,ad,cnt,em,image_r_p,id])
                  messages.success(request, 'Job updated successfully.')
                  return redirect('manage_jobs')

      return render(request, 'admin/edit_jobs.html', {'job': job})

def faq(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        q="select * from faq"
        cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'message': row[3],
            }
            for row in data
        ]
    return render(request, 'admin/faq.html', {'faqs': datalist})


def delete_faq(request, id):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as c:
        q="delete from faq where id=%s"
        c.execute(q,[id])
        messages.success(request, 'Message deleted successfully.')
    return redirect('faq')

def delete_issue(request, id):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as c:
        q="delete from issues where id=%s"
        c.execute(q,[id])
        messages.success(request, 'Issue deleted successfully.')
    return redirect('issues')

def issues(request):
    if not request.session.get('username'):
        return redirect('adlogin')
    with connection.cursor() as cursor:
        q="select * from issues"
        cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'description': row[3],
                'image': row[4],
            }
            for row in data
        ]
    return render(request, 'admin/issues.html', {'issues': datalist})


def logout(request):
    if 'username' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out successfully.')
        return redirect('adlogin')





##-----CLIENT VIEWS------##


def user_register(request):
    if request.session.get('user_username'):
        return redirect('user_home')
    with connection.cursor() as cursor:
        if request.method == 'POST':
            fn=request.POST.get('name')
            em=request.POST.get('email')
            cn=request.POST.get('contact')
            ct=request.POST.get('city')
            pw=request.POST.get('password')
            q="insert into aduser(name,email,contact,city,password) values(%s,%s,%s,%s,%s)"
            cursor.execute(q,[fn,em,cn,ct,pw])
            messages.success(request, 'Registration successful. Please login.')
            return redirect('user_login')
    return render(request, 'client/user_register.html')


def user_login(request):
    if request.session.get('user_username'):
        return redirect('user_home')
    if request.method == 'POST':
        um=request.POST.get('name')
        pw=request.POST.get('password')
        with connection.cursor() as cursor:
            q="select * from aduser where name=%s and password=%s"
            cursor.execute(q,[um,pw])
            data=cursor.fetchone()
            if data:
                request.session ['user_username']=data[1]
                messages.success(request, 'you are successfully logged in')
                return render(request, 'client/user_home.html')
            else:
                 return render(request, 'client/user_login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'client/user_login.html')


def user_home(request):
    return render(request, 'client/user_home.html')


def user_jobs(request):
     # build list of companies the current user already applied to (by name)
     applied_companies = set()
     username = request.session.get('user_username')
     if username:
         with connection.cursor() as cursor:
             q="select company from applied_job where name=%s"
             cursor.execute(q,[username])
             rows = cursor.fetchall()
             applied_companies = {r[0] for r in rows}

     # get search parameters
     job_title = request.GET.get('job_title', '').strip()
    

     with connection.cursor() as cursor:
        if job_title:
            # build dynamic query with filters
            q = "select * from adjobs where position like %s"
            params = []
            
            if job_title:
                params.append(f"%{job_title}%")
            cursor.execute(q, params)
        else:
            q="select * from adjobs"
            cursor.execute(q)
        data=cursor.fetchall()
        datalist=[
            {
                'category': row[1],
                'position': row[2],
                'company': row[3],
                'address': row[4],
                'contact': row[5],
                'email': row[6],
                'image': row[7],
            }
            for row in data
        ]
     return render(request, 'client/user_jobs.html', {'jobs': datalist, 'applied_companies': applied_companies})


def user_about(request):   
    return render(request, 'client/user_about.html')


def user_contact(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nm=request.POST.get('name')
            em=request.POST.get('email')
            msg=request.POST.get('message')
            q="insert into faq(name,email,message) values(%s,%s,%s)"
            cursor.execute(q,[nm,em,msg])
            messages.success(request, 'Contact form submitted successfully.')
            return redirect('user_contact')
    return render(request, 'client/user_contact.html', {'message': 'Contact form submitted successfully'})


def user_apply_jobs(request):
    if not request.session.get('user_username'):
        messages.error(request, 'Please login to apply for jobs.')
        return redirect('user_login')
    with connection.cursor() as cursor:
        if request.method == 'POST':
          nm=request.POST.get('name')
          em=request.POST.get('email')
          cn=request.POST.get('contact')
          cat=request.POST.get('category')                  # added category field
          pos=request.POST.get('position')                  # added position field
          company=request.POST.get('company')                  # added company field
          img=request.FILES.get('image')

          image_r_p = None
          if img:
               image_path=os.path.join(settings.MEDIA_ROOT,"resume", img.name)
               os.makedirs(os.path.dirname(image_path), exist_ok=True)
               with open(image_path, 'wb') as f:
                     for chunk in img.chunks():
                          f.write(chunk)
               image_r_p="/myapp/static/images/resume/"+img.name
               
          # prevent duplicate application for same company by same user
          cursor.execute("select id from applied_job where name=%s and company=%s", [nm, company])
          if cursor.fetchone():
              messages.error(request, 'You have already applied to this company.')
              return redirect('user_jobs')

          # include position column in insert statement
          q="insert into applied_job(name,email,contact,category,position,company,image) values(%s,%s,%s,%s,%s,%s,%s)"
          cursor.execute(q,[nm,em,cn,cat,pos,company,image_r_p])
          messages.success(request, 'Job application submitted successfully.')
          return redirect('user_application')  # redirect home so message alert shows there
    # prefill position and company from query parameter if provided
    pos = request.GET.get('position', '')
    cat = request.GET.get('category', '')
    company = request.GET.get('company', '')
    username = request.session.get('user_username')
    user_email = ''
    user_contact = ''
    if username:
        with connection.cursor() as user_cursor:
            user_cursor.execute("select email, contact from aduser where name=%s", [username])
            row = user_cursor.fetchone()
            if row:
                user_email, user_contact = row[0], row[1]

    return render(request, 'client/user_apply_jobs.html', {
        'position': pos,
        'category': cat,
        'company': company,
        'name': username,
        'email': user_email,
        'contact': user_contact,
    })

    
def user_application(request):
    if not request.session.get('user_username'):
        return redirect('user_login')
    username = request.session.get('user_username')
    with connection.cursor() as cursor:
        q="select * from applied_job where name=%s"
        cursor.execute(q, [username])
        data=cursor.fetchall()
        datalist=[
            {
                'id': row[0],                # primary key
                'name': row[1],
                'email': row[2],
                'contact': row[3],
                'category': row[4],         # category stored as 4th column
                'position': row[5],
                'company': row[6],
                'image': row[7],            # resume path is last column
            }
            for row in data
        ]
    return render(request, 'client/user_application.html', {'applications': datalist})


def delete_application1(request, id):
    if not request.session.get('user_username'):
        return redirect('user_login')
    with connection.cursor() as c:
        q="delete from applied_job where id=%s"
        c.execute(q,[id])
        messages.success(request, 'Application deleted successfully.')
    return redirect('user_application')


def client_logout(request):
    if 'user_username' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out successfully.')
        return redirect('user_login')    
def help_center(request):
    return render(request, 'client/help_center.html')
def documentation(request):
    return render(request, 'client/documentation.html')
def report_issue(request, id=None):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nm = request.POST.get('name','').strip()
            em = request.POST.get('email','').strip()
            des = request.POST.get('issue','').strip()   # field name updated
            img = request.FILES.get('screenshot')        # file input name updated
            # simple validation
            if not nm or not em or not des:
                messages.error(request, 'Name, email and issue description are required.')
                return render(request, 'client/report_issue.html', {'id': id, 'name': nm, 'email': em, 'issue': des})
            image_r_p = None
            if img:
               image_path=os.path.join(settings.MEDIA_ROOT,"issues", img.name)
               os.makedirs(os.path.dirname(image_path), exist_ok=True)
               with open(image_path, 'wb') as f:
                     for chunk in img.chunks():
                          f.write(chunk)
               image_r_p="/myapp/static/images/issues/"+img.name
            q="insert into issues(name,email,description,image) values(%s,%s,%s,%s)"
            cursor.execute(q,[nm,em,des,image_r_p])
            messages.success(request, 'Issue reported successfully.')
            # redirect back, preserving id if provided
            if id is not None:
                return redirect('report_issue', id=id)
            return redirect('report_issue')
    return render(request, 'client/report_issue.html', {'id': id})
def privacy_policy(request):
    return render(request, 'client/privacy_policy.html')
def terms_services(request):
    return render(request, 'client/terms_services.html')
def cookie_policy(request):
    return render(request, 'client/cookie_policy.html')

    