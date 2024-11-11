from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import URL
from .forms import URLForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def add_url(request):
    if request.method == 'POST':
        if URL.objects.filter(user=request.user).count() < 5:
            form = URLForm(request.POST)
            if form.is_valid():
                url = form.save(commit=False)
                url.user = request.user
                url.save()
                return redirect('url_list')
        else:
            form = URLForm()  # Return a fresh form
            return render(request, 'add_url.html', {'form': form, 'error': 'Limit of 5 URLs reached.'})
    else:
        form = URLForm()  # If it's a GET request, provide an empty form
    return render(request, 'add_url.html', {'form': form})

@login_required
def url_list(request):
    # Filter URLs belonging to the logged-in user and order by creation date
    urls = URL.objects.filter(user=request.user).order_by('-created_at')
    
    # Create a paginator that shows 2 URLs per page
    paginator = Paginator(urls, 2)  # Change this to 2 for your requirement
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the paginated URLs
    return render(request, 'url_list.html', {'page_obj': page_obj})

@login_required
def edit_url(request, pk):
    url = URL.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = URLForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('url_list')
    else:
        form = URLForm(instance=url)
    return render(request, 'edit_url.html', {'form': form})

@login_required
def delete_url(request, pk):
    url = URL.objects.get(pk=pk, user=request.user)
    url.delete()
    return redirect('url_list')


@login_required
def search_url(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if AJAX request
        query = request.GET.get('q', '')
        urls = URL.objects.filter(user=request.user, title__icontains=query)
        
        # Render the partial HTML with the search results
        html = render_to_string('url_list_partial.html', {'urls': urls}, request=request)
        return JsonResponse({'html': html})  # Return the rendered HTML as JSON

    return redirect('url_list')

@login_required
def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
    return render(request, 'logout.html', {'user': request.user})