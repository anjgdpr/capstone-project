from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from .models import Book
from django.core.paginator import Paginator
from django.db.models import Q 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
import __main__, os 
import pickle 
import pandas as pd 
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt


def index (request): 
    return render(request, 'books/index.html')

def loginview(request):
    form = LoginForm(request.POST or None)
    return render(request, 'books/login.html', {'form': form})

def signup(request): 
    form = SignUpForm(request.POST or None)
    return render(request, 'books/signup.html', {'form': form})

def register(request): #user registration
    error_msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            error_msg = 'user created'
            return redirect('loginview')
        else:
            error_msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'books/signup.html', {'form': form, 'error_msg': error_msg})

def processlogin(request): #login auth
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('/books/lib_index')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('s_browse')
            else:
                error_message = 'Invalid credentials'
        else:
            error_message = 'Login Failed'
    return render(request, 'books/login.html', {'form': form, 'error_message': error_message})
   
def processlogout(request): #logout
    logout(request)
    return HttpResponseRedirect ('/books/login')

@login_required(login_url='/books/login') #admin index
def lib_index(request):
    return render(request, 'books/lib_index.html')

def contact(request): #contact page 
    return render(request, 'books/contact.html')

def l_browse (request): #locked browse
    return render(request, 'books/l-browse.html')

@login_required(login_url='/books/login') #admin browse
def browse (request): 
    book_list = Book.objects.all().order_by('-pub_year')
    paginator = Paginator(book_list, 9)
    page_number = request.GET.get('page')
    book_list = paginator.get_page(page_number)
    return render(request, 'books/browse.html', {'page_obj': book_list})

@login_required(login_url='/books/login') #student browse
def s_browse (request): 
    book_list = Book.objects.all().order_by('-pub_year')
    paginator = Paginator(book_list, 9)
    page_number = request.GET.get('page')
    book_list = paginator.get_page(page_number)
    return render(request, 'books/s_browse.html', {'page_obj': book_list})

@login_required(login_url='/books/login') #admin paper detail
def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist: 
        raise Http404("Title does not exist")
    return render(request, 'books/detail.html', {'book':book})

def s_detail(request, book_id): #student paper detail
    #cosine_sim = pickle.load(open('cosine_sim-v5.pkl','rb'))
    #workpath = 'C:/Users/angel/Desktop/libraryapp'
    #data = open(os.path.join(workpath, 'try.csv'), 'rb')
    #data = pd.read_csv(data)
    #data = pd.read_csv('try.csv', sep=',', encoding='utf-8')
    try:
        book = Book.objects.get(pk=book_id)
        fav = True 
        if book.favorites.filter(id=request.user.id).exists():
            fav=False
    
        #def recommendations(book_id,n, cosine_sim = cosine_sim):
            #recommended_books = []
            #idx = data.loc[data['book_id'] == book_id].index[0]
            #score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
            #top_n_indexes = list(score_series.iloc[1:n+1].index)
            #for i in top_n_indexes:
                #recommended_books.append(list(data.index)[i]) # ['Title']
                #print(top_n_indexes)
            #return recommended_books
        #book_id = Book.objects.get(pk=book_id)
        #recommend = recommendations(book_id, 3)
    except Book.DoesNotExist: 
        raise Http404("Title does not exist")    
    return render (request, 'books/s_detail.html', {'book':book, 'fav':fav}) #, 'recommend':recommend


#def recommend(request, book_id): 
    book = Book.objects.get(pk=book_id)
    cosine_sim = pickle.load(open('cosine_sim-v4.pkl','rb'))
    data = pd.read_csv('new-data.csv', sep=',', encoding='utf-8')
        
    def recommendations(id,n, cosine_sim = cosine_sim):
        recommended_books = []
        idx = data.loc[data['id'] == id].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        top_n_indexes = list(score_series.iloc[1:n+1].index)
        for i in top_n_indexes:
            recommended_books.append(list(data.index)[i])
        return recommended_books
    recommend = recommendations(book, 3)
    return render (request, 'books/s_detail.html', {'book':book, 'recommend':recommend})


@login_required(login_url='/books/login') #catalog page
def add(request): 
    return render(request,'books/add.html')

def processadd(request): #add paper function
    title = request.POST.get('title')
    authors = request.POST.get('author')
    month = request.POST.get('Month')
    year = request.POST.get('Year')
    type = request.POST.get('Type')
    college = request.POST.get('slct1')
    course = request.POST.get('slct2')
    abstract = request.POST.get('txtArea')
    if request.FILES.get('image'): 
        book_pic = request.FILES.get('image')
    else: 
        book_pic = 'book_pic/book_image.jpg'
    try: 
        n = Book.objects.get(book_title=title)
        #number already exists 
        return render(request, 'books/add.html', {
            'error_message': "Title already exists: " + title
        })
    except ObjectDoesNotExist: 
        book = Book.objects.create(book_image=book_pic, book_title=title, book_authors=authors,pub_month=month, pub_year=year, book_college=college, book_type=type, book_course=course, book_abstract=abstract)
        book.save()
        return HttpResponseRedirect('/books/browse')
    
def edit(request,book_id): #edit page 
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist: 
        raise Http404("Title does not exist")
    return render(request, 'books/edit.html', {'book':book})

def processedit(request,book_id): #save edited details 
    book = get_object_or_404(Book, pk=book_id)
    book_pic = request.FILES.get('image')
    try: 
        title = request.POST.get('title')
        authors = request.POST.get('author')
        month = request.POST.get('Month')
        year = request.POST.get('Year')
        college = request.POST.get('slct1')
        course = request.POST.get('slct2')
        type = request.POST.get('Type')
        abstract = request.POST.get('txtArea')
    except (KeyError, Book.DoesNotExist): 
        return render(request, 'books/detail.html', {
            'book': book, 
            'error_message': "Problem updating record",
        })
    else: 
        book_profile = Book.objects.get(id=book_id)
        book_profile.book_title = title
        book_profile.book_authors = authors
        book_profile.pub_month = month 
        book_profile.pub_year = year
        book_profile.book_type = type 
        book_profile.book_college = college
        book_profile.book_course = course 
        book_profile.book_abstract = abstract   
        if book_pic: 
            book_profile.book_image = book_pic
            book_profile.save()
        else: book_profile.save()
        return HttpResponseRedirect(reverse('detail', args=(book_id,)))

def search (request): #lookup for admin 
    term = request.GET.get('search', '')
    book_list = Book.objects.filter( Q (book_title__icontains=term) | Q (book_authors__icontains=term) | Q (pub_year__icontains=term) | Q (book_college__icontains=term)  | Q (book_course__icontains=term) | Q (book_abstract__icontains=term)).order_by('-pub_year')
    
    paginator = Paginator(book_list, 9)
    page_number = request.GET.get('page')
    book_list = paginator.get_page(page_number)
    return render(request, 'books/browse.html', {'page_obj': book_list})

@csrf_exempt
def s_search (request): #lookup for student
    term = request.GET.get('search', '')
    book_list = Book.objects.filter( Q (book_title__icontains=term) | Q (book_authors__icontains=term) | Q (pub_year__icontains=term) | Q (book_college__icontains=term)  | Q (book_course__icontains=term) | Q (book_abstract__icontains=term)).order_by('-pub_year')
    
    paginator = Paginator(book_list, 9)
    page_number = request.GET.get('page')
    book_list = paginator.get_page(page_number)
    return render(request, 'books/s_browse.html', {'page_obj': book_list})

@csrf_exempt
def filterview(request): #student filter 
    qs = Book.objects.all().order_by('-pub_year')
    sort_by = request.GET.get('sortb')
    college = request.GET.get('slct1')
    course = request.GET.get('slct2')
    section = request.GET.get('Type')
    
    if sort_by == 'Year': 
        qs = qs.order_by('-pub_year')
    elif sort_by == '2017': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2017) )
    elif sort_by == '2018': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2018) )
    elif sort_by == '2019': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2019) )
    elif sort_by == '2020': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2020) )
    elif sort_by == '2021': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2021) )
    if college != 'Colleges' and college is not None:
        qs = qs.filter(book_college=college)
    if course != '' and course is not None:
        qs = qs.filter(book_course=course)
    if section != 'Section' and  section is not None:
        qs = qs.filter(book_type=section)
        
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    qs = paginator.get_page(page_number)
        
    context = {
        'page_obj': qs,
    }
    return render(request, 'books/s_browse.html', context)

def libfilterview(request): #admin filter
    qs = Book.objects.all().order_by('-pub_year')
    sort_by = request.GET.get('sortb')
    college = request.GET.get('slct1')
    course = request.GET.get('slct2')
    section = request.GET.get('Type')
    
    if sort_by == 'Year': 
        qs = qs.order_by('-pub_year')
    elif sort_by == '2017': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2017) )
    elif sort_by == '2018': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2018) )
    elif sort_by == '2019': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2019) )
    elif sort_by == '2020': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2020) )
    elif sort_by == '2021': 
        qs = Book.objects.filter ( Q (pub_year__icontains=2021) )
    if college != 'Colleges' and college is not None:
        qs = qs.filter(book_college=college)
    if course != '' and course is not None:
        qs = qs.filter(book_course=course)
    if section != 'Section' and  section is not None:
        qs = qs.filter(book_type=section)
        
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    qs = paginator.get_page(page_number)
        
    context = {
        'page_obj': qs,
    }
    return render(request, 'books/browse.html', context)

def favorite_add(request, id): 
    book = get_object_or_404(Book, id=id)
    fav = bool 
    if book.favorites.filter(id=request.user.id).exists():
        fav=True
        book.favorites.remove(request.user)
    else:
        book.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'], {'fav':fav})

def favorite_list(request): #favorites page
    new = Book.objects.filter(favorites=request.user)
    return render(request,'books/favorites.html',{'new': new})



