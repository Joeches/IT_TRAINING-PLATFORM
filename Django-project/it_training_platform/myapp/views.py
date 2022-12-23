#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, CompletedLesson
from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lesson_set.all()
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        enrollment.save()
        return redirect('course_detail', slug=slug)
    else:
        return redirect('enrollment_error')

def enrollment_error(request):
    return render(request, 'courses/enrollment_error.html')

@login_required
def complete_lesson(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    completed_lesson, created = CompletedLesson.objects.get_or_create(student=request.user, lesson=lesson)
    if created:
        completed_lesson.save()
        return redirect('lesson_detail', course_slug=course_slug, lesson_slug=lesson_slug)
    else:
        return redirect('completion_error')

def completion_error(request):
    return render(request, 'courses/completion_error.html')
