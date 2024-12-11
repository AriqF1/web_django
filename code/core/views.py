from django.shortcuts import render, get_object_or_404
from fastapi import APIRouter
from .models import Register
from models import User 
from core.apiv1 import apiv1
from .models import Course, CourseContent, Comment
from django.db.models import Max, Min, Avg
from django.http import JsonResponse
from django.db.models import Count
from .schemas import Kalkulator
from ninja import Router


def course_list(request):
    courses = Course.objects.all()  # mengambil semua course dari database
    return render(request, 'core/course_list.html', {'courses': courses})

# views.py
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    course_contents = CourseContent.objects.filter(course_id=course)
    comments = Comment.objects.filter(content_id__course_id=course)
    return render(request, 'course_detail.html', {
        'course': course,
        'course_contents': course_contents,
        'comments': comments,
    })
def allCourse(request):
    allCourse = Course.objects.all()
    result = []
    for course in allCourse:
        record = {'id': course.id, 'name': course.name, 
                  'description': course.description, 
                  'price': course.price,
                  'teacher': {
                      'id': course.teacher.id,
                      'username': course.teacher.username,
                      'email': course.teacher.email,
                      'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
                  }}
        result.append(record)
    return JsonResponse(result, safe=False)

def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    result = {
        'course_count': courses.count(),
        'courses': stats
    }
    return JsonResponse(result, safe=False)

def courseMemberStat(request):
    courses = Course.objects.filter(description__icontains='python') \
                            .annotate(member_num=Count('coursemember'))
    course_data = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'price': course.price,
            'member_count': course.member_num
        }
        course_data.append(record)
    result = {
        'data_count': len(course_data),  # Menggunakan len karena course_data adalah list
        'data': course_data
    }
    return JsonResponse(result, safe=False)

def courseDetail(request, course_id):
    try:
        # Mengambil objek course berdasarkan course_id
        course = Course.objects.get(id=course_id)
        
        # Menyiapkan data untuk dikembalikan
        result = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            },
            'created_at': course.created_at,
            'updated_at': course.updated_at,
        }

        # Mengembalikan data dalam format JSON
        return JsonResponse(result, safe=False, json_dumps_params={'indent': 4})
    except Course.DoesNotExist:
        # Jika course tidak ditemukan
        return JsonResponse({'error': 'Course not found'}, status=404)
    
@apiv1.get('calc/{nil1}/{opr}/{nil2}')
def calculator(request, nil1:int, opr:str, nil2:int):
    hasil = nil1 + nil2
    if opr == '-':
        hasil = nil1 - nil2
    elif opr == 'x':
        hasil = nil1 * nil2
    
    return {'nilai1': nil1, 'nilai2': nil2, 'operator': opr, 'hasil': hasil}

@apiv1.post('hello/')
def helloPost(request):
    if 'nama' in request.POST:
        return f"Selamat menikmati ya {request.POST['nama']}"
    return "Selamat tinggal dan pergi lagi"

@apiv1.put('users/{id}')
def userUpdate(request, id:int):
    return f"User dengan id {id} Nama aslinya adalah Herdiono kemudian diganti menjadi {request.body}"

@apiv1.delete('users/{id}')
def userDelete(request, id:int):
    return f"Hapus user dengan id: {id}"



apiv1 = Router()

@apiv1.post('calc')
def postCalc(request, skim: Kalkulator):
    skim.hasil = skim.calcHasil()
    return skim

 # Misalkan User adalah model untuk database Anda

router = APIRouter()

@router.post("/register/", response_model=User)
def register(data: Register):
    new_user = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return new_user

