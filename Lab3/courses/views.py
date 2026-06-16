from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Course, Category
from .forms import CourseForm

# 1. Lista de cursuri + Filtrare & Căutare
def course_list(request):
    courses = Course.objects.all().order_by('-year', 'title')
    categories = Category.objects.all().order_by('name')
    
    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
        
    query = request.GET.get('q', '')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(instructor__icontains=query)
        )
        
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
    })

# 2. Detalii curs
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

# 3. Adăugare curs (necesită login)
@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Add'})

# 4. Modificare curs (Exercițiu Secțiunea 2)
@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit'})

# 5. Ștergere curs (Exercițiu Secțiunea 2)
@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# 6. Pagina pentru cursurile dintr-o categorie (Exercițiu Final)
def category_courses(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses = category.courses.all().order_by('-year', 'title')
    return render(request, 'courses/category_courses.html', {
        'category': category,
        'courses': courses
    })

# 7. API JSON pentru toate cursurile
def api_courses(request):
    courses = Course.objects.all().order_by('-year', 'title')
    data = [
        {
            'id': c.pk,
            'title': c.title,
            'instructor': c.instructor,
            'year': c.year,
            'category': c.category.name,
            'credits': c.credits,
        }
        for c in courses
    ]
    return JsonResponse(data, safe=False)

# 8. API JSON pentru un singur curs (Exercițiu Secțiunea 7)
def api_course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    data = {
        'id': course.pk,
        'title': course.title,
        'instructor': course.instructor,
        'year': course.year,
        'category': course.category.name,
        'credits': course.credits,
    }
    return JsonResponse(data)