# Create your views here.
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib
from dormsys.models import *
from dormsys.config import *
from datetime import datetime


# index
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        return HttpResponse("error")


# login
def login(request):
    # 处理GET请求
    if request.method == 'GET':
        return render(request, 'login.html')
    #     #1, 首先检查session，判断用户是否第一次登录，如果不是，则直接重定向到首页
    #     if 'username' in request.session:  #request.session 类字典对象
    #         return HttpResponseRedirect('/index/allbook')
    #     #2, 然后检查cookie，是否保存了用户登录信息
    #     if 'username' in request.COOKIES:
    #         #若存在则赋值回session，并重定向到首页
    #         request.session['username'] = request.COOKIES['username']
    #         return HttpResponseRedirect('/index/allbook')
    #     #不存在则重定向登录页，让用户登录
    #     return render(request, 'user/login.html')
    # # 处理POST请求

    elif request.method == 'POST':
        user_id = request.POST.get('inputEmail3')
        password = request.POST.get('inputPassword3')

        # m = hashlib.md5()
        # m.update(password.encode())
        # password_m = m.hexdigest()
        # #判断输入是否其中一项为空或者格式不正确
        # if not username or not password:
        #     error = '你输入的用户名或者密码错误 !'
        #     return render(request, 'user/login.html', locals())
        # #若输入没有问题则进入数据比对阶段，看看已经注册的用户中是否存在该用户
        users = User.objects.filter(member_id=user_id, password=password)
        # 由于使用了filter, 所以返回值user是一个数组，但是也要考虑其为空的状态，即没有查到该用户
        if not users:
            error = '用户不存在或用户密码输入错误!!'
            print(error)
            return HttpResponse(error)
        # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
        else:
            users = users[0]
            request.session['user_id'] = user_id
            # response = HttpResponseRedirect('/index/allbook')
            # #检查post 提交的所有键中是否存在 isSaved 键
            # if 'isSaved' in request.POST.keys():
            #     #若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
            #     response.set_cookie('username', username, 60*60*24*7)

            if users.type == STUDENT:
                rep = redirect('/dormsys/student_main')
            elif users.type == TUTOR:
                rep = redirect('/dormsys/tutor_main')
            elif users.type == SUPERVISOR:
                rep = redirect('/dormsys/supervisor_main')

            rep.set_cookie(key='user_id', value=user_id, max_age=1800)
            return rep


# logout
def logout(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            del request.COOKIES['user_id']
        else:
            return redirect('/dormsys/login')

        rep = redirect('/dormsys/login')
        rep.delete_cookie('user_id')

        return rep
    else:
        pass


# student
def student_main(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        student = _get_student_info(student_number)
        announcement = Announcement.objects.all()[len(Announcement.objects.all()) - 1]

        return render(request, "student_main.html", {"student": student, 'announcement': announcement})
    else:
        pass


def change_student_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            student = _get_student_info(student_number)
            return render(request, "change_student_info.html", {'student': student})
        else:
            return HttpResponse("have not logged in")

    else:

        name = request.POST.get("name")
        student_number = request.POST.get("id")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        deparment_number = request.POST.get("course")
        Student.objects.filter(student_number=student_number).update(student_number=student_number, name=name,
                                                                     gender=gender, phone_number=phone_number)
        Department_Student.objects.filter(student_number=student_number).update(department_number=deparment_number)

        student = _get_student_info(student_number)

        return render(request, "student_main.html", {"student": student})


def change_or_add_emergency_contact(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            student = _get_student_info(student_number)

            return render(request, "change_or_add_emergency_contact.html", {'student': student})
        else:
            return HttpResponse("have not logged in")
    else:
        student_number = request.COOKIES['user_id']
        student_number = request.POST.get("id")

        emergency_name = request.POST.get("emergency_name")
        phone_number = request.POST.get("phone_number")
        relation = request.POST.get("connection")

        print(student_number)
        print(emergency_name)
        print(relation)

        e = EmergencyContact.objects.filter(student_number=student_number)
        print(e)
        if len(e) != 0:
            e.update(student_number=student_number, emergency_name=emergency_name, phone_number=phone_number,
                     relation=relation)
        else:

            EmergencyContact.objects.create(student_number=student_number, emergency_name=emergency_name,
                                            phone_number=phone_number, relation=relation)

        student = _get_student_info(student_number)

        return render(request, "student_main.html", {"student": student})


def deal_with_dorm(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            return render(request, "deal_with_dorm.html")
        else:
            return HttpResponse("have not logged in")
    else:
        pass


def search_dorm_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        student = _get_student_info(student_number)

        dd = DormDistribution.objects.get(student_number=student_number)
        your_room_number = dd.room_number
        your_apartment_number = dd.apartment_number

        all_student = []

        for s in DormDistribution.objects.filter(room_number=your_room_number,
                                                 apartment_number=your_apartment_number):
            student = _get_student_info(s.student_number)
            all_student.append(student)

        dorm_info = {}
        dorm_info['apartment_name'] = Apartment.objects.get(apartment_number=your_apartment_number).apartment_name
        dorm_info['region'] = Apartment.objects.get(apartment_number=your_apartment_number).region
        dorm_info['room_number'] = your_room_number
        # dorm_info = dict(dorm_info)
        # dorm_info['room_number'] = your_room_number
        supervisor = {}
        supervisor['name'] = DormAdmin.objects.get(apartment_number=your_apartment_number).name
        supervisor['supervisor_number'] = DormAdmin.objects.get(
            apartment_number=your_apartment_number).supervisor_number
        supervisor['phone_number'] = DormAdmin.objects.get(apartment_number=your_apartment_number).phone_number
        supervisor['apartment_name'] = Apartment.objects.get(apartment_number=your_apartment_number).apartment_name
        supervisor['region'] = Apartment.objects.get(apartment_number=your_apartment_number).region

        return render(request, "search_dorm_info.html",
                      {"all_student": all_student, "dorm_info": dorm_info, "supervisor": supervisor})
    else:
        pass


def search_announcement(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        all_announcements = []

        for a in Announcement.objects.all():
            annoucement = {}
            annoucement['issue_time'] = a.issue_time
            annoucement['content'] = a.content
            annoucement['name'] = DormAdmin.objects.get(supervisor_number=a.supervisor_number).name
            all_announcements.append(annoucement)

        return render(request, "search_announcement.html", {"all_announcements": all_announcements})
    else:
        pass


def enter_dorm(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            return render(request, "enter_dorm.html")
        else:
            return HttpResponse("have not logged in")

    else:
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        name = Student.objects.get(student_number=student_number).name
        region = request.POST.get("region")
        apartment_name = request.POST.get("apartment_name")
        room_number = request.POST.get("room_number")

        # EnterDorm.objects.create(student_number=student_number, region=region, apartment_name=apartment_name,
        #                          room_number=room_number, state=NOT_PROCESSED)

        Approval.objects.create(student_number=student_number, name=name, region=region,
                                apartment_name=apartment_name,
                                room_number=room_number, state=NOT_PROCESSED, type=ENTER)

        student = _get_student_info(student_number)

        return render(request, "student_main.html", {"student": student})


def delete_dorm(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            student = _get_student_info(student_number)
            return render(request, "delete_dorm.html", {'student': student})
        else:
            return HttpResponse("have not logged in")

    else:
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        name = request.POST.get("name")
        student_number = request.POST.get("student_number")

        room_number = _get_student_info(student_number)['room_number']
        region = _get_student_info(student_number)['region']

        # EnterDorm.objects.create(student_number=student_number,room_number=room_number)

        # QuitDorm.objects.create(student_number=student_number, region=region,
        #                         room_number=room_number, state=NOT_PROCESSED)

        Approval.objects.create(student_number=student_number, name=name, region=region,
                                room_number=room_number, state=NOT_PROCESSED, type=DELETE)

        student = _get_student_info(student_number)

        return render(request, "student_main.html", {"student": student})


def change_dorm(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
            student = _get_student_info(student_number)
            return render(request, "change_dorm.html", {'student': student})
        else:
            return HttpResponse("have not logged in")

    else:
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        name = request.POST.get("name")
        student_number = request.POST.get("student_number")
        region = request.POST.get("region")
        apartment_name = request.POST.get("apartment_name")
        room_number = request.POST.get("room_number")

        # EnterDorm.objects.create(student_number=student_number,room_number=room_number)

        # EnterDorm.objects.create(student_number=student_number, region=region, apartment_name=apartment_name,
        #                          room_number=room_number, state=NOT_PROCESSED)

        Approval.objects.create(student_number=student_number, name=name, region=region,
                                apartment_name=apartment_name,
                                room_number=room_number, state=NOT_PROCESSED, type=CHANGE)

        student = _get_student_info(student_number)

        return render(request, "student_main.html", {"student": student})


def search_empty_dorm1(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        room = Room.objects.filter(rest_num__gt=0)
        all_rooms = []
        for r in room:
            room_info = {}
            room_info['region'] = Apartment.objects.get(apartment_number=r.apartment_number).region
            room_info['apartment_name'] = Apartment.objects.get(apartment_number=r.apartment_number).apartment_name
            room_info['room_number'] = r.room_number
            all_rooms.append(room_info)

        return render(request, "search_empty_dorm1.html",
                      {"all_rooms": all_rooms})
    else:
        pass


def search_empty_dorm2(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        room = Room.objects.filter(rest_num__gt=0)
        all_rooms = []
        for r in room:
            room_info = {}
            room_info['region'] = Apartment.objects.get(apartment_number=r.apartment_number).region
            room_info['apartment_name'] = Apartment.objects.get(apartment_number=r.apartment_number).apartment_name
            room_info['room_number'] = r.room_number
            all_rooms.append(room_info)

        return render(request, "search_empty_dorm1.html",
                      {"all_rooms": all_rooms})
    else:
        pass


def matter_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            student_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        all_matters = Approval.objects.filter()

        return render(request, "matter_info.html",
                      {"all_matters": all_matters})
    else:
        pass


# tutor

def tutor_main(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        tutor = _get_tutor_info(tutor_number)

        announcement = Announcement.objects.all()[len(Announcement.objects.all()) - 1]

        return render(request, "tutor_main.html", {"tutor": tutor, 'announcement': announcement})
    else:
        pass


def change_tutor_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']

            tutor = _get_tutor_info(tutor_number)

            return render(request, "change_tutor_info.html", {'tutor': tutor})
        else:
            return HttpResponse("have not logged in")

    else:

        name = request.POST.get("name")
        tutor_number = request.POST.get("tutor_number")
        phone_number = request.POST.get("phone_number")
        deparment_number = request.POST.get("deparment_number")
        Tutor.objects.filter(tutor_number=tutor_number).update(tutor_number=tutor_number, name=name,
                                                               phone_number=phone_number)

        tutor = _get_tutor_info(tutor_number)

        return render(request, "tutor_main.html", {"tutor": tutor})


def search_student_info_from_tutor(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            pass
        else:
            return HttpResponse("have not logged in")

        return render(request, "search_student_info_from_tutor.html")
    else:

        tutor_number = request.COOKIES['user_id']

        student_number = request.POST.get("student_number")
        student = _get_student_info(student_number)
        emergency = _get_emergency_info(student_number)

        sum = len(Student.objects.filter(tutor_number=tutor_number))

        return render(request, "show_student_info_from_tutor.html",
                      {'student': student, 'emergency': emergency, 'sum': sum})


def allocate_dorm(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']
            return render(request, "allocate_dorm.html")
        else:
            return HttpResponse("have not logged in")

    else:

        name = request.POST.get("name")
        student_number = request.POST.get("student_number")
        region = request.POST.get("region")
        apartment_number = request.POST.get("apartment_number")
        room_number = request.POST.get("room_number")
        DormDistribution.objects.create(student_number=student_number, room_number=room_number,
                                        apartment_number=apartment_number)

        return render(request, "allocate_dorm.html")


def approve_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']

            all_matters = Approval.objects.filter(state=NOT_PROCESSED)

            return render(request, "approve_info.html", {'all_matters': all_matters})
        else:
            return HttpResponse("have not logged in")
    else:

        pass


def approve_agree(request, matter_id=None):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']

            matter = Approval.objects.get(id=matter_id)
            student_number = matter.student_number
            student = _get_student_info(student_number)

            return render(request, "approve_agree.html", {'matter': matter, 'student': student})
        else:
            return HttpResponse("have not logged in")
    else:
        Approval.objects.filter(id=matter_id).update(state=AGREED)
        matter = Approval.objects.get(id=matter_id)

        if (matter.type == ENTER):
            apartment_number = Apartment.objects.get(apartment_name=matter.apartment_name).apartment_number
            DormDistribution.objects.create(student_number=matter.student_number, apartment_number=apartment_number,
                                            room_number=matter.room_number)
        elif (matter.type == CHANGE):
            apartment_number = Apartment.objects.get(apartment_name=matter.apartment_name).apartment_number
            DormDistribution.objects.filter(student_number=matter.student_number).update(
                student_number=matter.student_number, apartment_number=apartment_number, room_number=matter.room_number)
        elif (matter.type == DELETE):
            DormDistribution.objects.get(student_number=matter.student_number).delete()

        all_matters = Approval.objects.filter(state=NOT_PROCESSED)
        return render(request, "approve_info.html", {"all_matters": all_matters})


def approve_disagree(request, matter_id=None):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            tutor_number = request.COOKIES['user_id']

            matter = Approval.objects.get(id=matter_id)
            student_number = matter.student_number
            student = _get_student_info(student_number)

            return render(request, "approve_disagree.html", {'matter': matter, 'student': student})
        else:
            return HttpResponse("have not logged in")
    else:
        Approval.objects.filter(id=matter_id).update(state=DISAGREED)

        all_matters = Approval.objects.filter(state=NOT_PROCESSED)
        return render(request, "approve_info.html", {"all_matters": all_matters})


def search_no_dorm_student(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            pass
        else:
            return HttpResponse("have not logged in")

        not_alloc_students = []
        students = Student.objects.all()

        for s in students:
            t = DormDistribution.objects.filter(student_number=s.student_number)

            if not t.exists():
                not_alloc_s = Student.objects.get(student_number=s.student_number)
                not_alloc_students.append(not_alloc_s)

        sum = len(not_alloc_students)
        return render(request, "search_no_dorm_student.html", {'all_students': not_alloc_students, 'sum': sum})
    else:
        student_number = request.POST.get("student_number")
        student = _get_student_info(student_number)
        emergency = _get_emergency_info(student_number)

        return render(request, "search_no_dorm_student.html", {'student': student, 'emergency': emergency})


# supervisor
def supervisor_main(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            supervisor_number = request.COOKIES['user_id']
        else:
            return HttpResponse("have not logged in")

        supervisor = _get_supervisor_info(supervisor_number)

        announcement = Announcement.objects.all()[len(Announcement.objects.all()) - 1]

        return render(request, "supervisor_main.html", {"supervisor": supervisor,'announcement':announcement})
    else:
        pass


def change_supervisor_info(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            supervisor_number = request.COOKIES['user_id']
            supervisor = _get_supervisor_info(supervisor_number)
            return render(request, "change_supervisor_info.html", {'supervisor': supervisor})
        else:
            return HttpResponse("have not logged in")

    else:

        name = request.POST.get("name")
        supervisor_number = request.POST.get("supervisor_number")
        phone_number = request.POST.get("phone_number")
        apartment_number = request.POST.get("apartment_number")
        region = request.POST.get("region")  # FIXME
        DormAdmin.objects.filter(supervisor_number=supervisor_number).update(supervisor_number=supervisor_number,
                                                                             name=name,
                                                                             apartment_number=apartment_number,
                                                                             phone_number=phone_number)

        supervisor = _get_supervisor_info(supervisor_number)

        return render(request, "supervisor_main.html", {"supervisor": supervisor})


def search_student_info_from_supervisor(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            pass
        else:
            return HttpResponse("have not logged in")

        return render(request, "search_student_info_from_tutor.html")
    else:
        student_number = request.POST.get("student_number")
        student = _get_student_info(student_number)
        emergency = _get_emergency_info(student_number)

        supervisor_number = request.COOKIES['user_id']
        your_apartment_number = DormAdmin.objects.get(supervisor_number=supervisor_number).apartment_number
        student_sum = len(DormDistribution.objects.filter(apartment_number=your_apartment_number))
        dorm_sum = len(Room.objects.filter(apartment_number=your_apartment_number))
        empty_dorm_sum = dorm_sum - len(Room.objects.filter(apartment_number=your_apartment_number, rest_num=0))

        return render(request, "show_student_info_from_supervisor.html",
                      {'student': student, 'emergency': emergency, 'student_sum': student_sum, 'dorm_sum': dorm_sum,
                       'empty_dorm_sum': empty_dorm_sum})


def make_announcement(request):
    if request.method == "GET":
        if 'user_id' in request.COOKIES.keys():
            pass
        else:
            return HttpResponse("have not logged in")

        return render(request, "make_announcement.html")
    else:
        supervisor_number = request.COOKIES['user_id']
        supervisor_name = DormAdmin.objects.get(supervisor_number=supervisor_number).name
        content = request.POST.get("content")
        issue_time = datetime.now()
        Announcement.objects.create(content=content, supervisor_number=supervisor_number, issue_time=issue_time)

        supervisor = _get_supervisor_info(supervisor_number)

        return render(request, "supervisor_main.html", {'supervisor': supervisor})


# private functions

def _get_student_info(student_number):
    student = {}

    s = Student.objects.get(student_number=student_number)

    student['name'] = s.name
    student['student_number'] = student_number
    student['gender'] = s.gender
    department_number = Department_Student.objects.get(student_number=student_number).department_number
    department_name = Department.objects.get(department_number=department_number).department_name
    student['department_name'] = department_name
    student['in_year'] = s.in_year
    student['phone_number'] = s.phone_number

    student['room_number'] = DormDistribution.objects.get(student_number=student_number).room_number
    apartment_number = DormDistribution.objects.get(student_number=student_number).apartment_number
    student['apartment_number'] = apartment_number

    student['apartment_name'] = Apartment.objects.get(apartment_number=apartment_number).apartment_name
    student['region'] = Apartment.objects.get(apartment_number=apartment_number).region

    return student


def _get_tutor_info(tutor_number):
    tutor = {}

    t = Tutor.objects.get(tutor_number=tutor_number)

    tutor['name'] = t.name
    tutor['tutor_number'] = tutor_number

    tutor['department_name'] = Department.objects.get(department_number=t.department_number).department_name
    tutor['phone_number'] = t.phone_number

    return tutor


def _get_supervisor_info(supervisor_number):
    supervisor = {}

    s = DormAdmin.objects.get(supervisor_number=supervisor_number)

    supervisor['name'] = s.name
    supervisor['supervisor_number'] = supervisor_number

    supervisor['region'] = Apartment.objects.get(apartment_number=s.apartment_number).region
    supervisor['apartment_number'] = s.apartment_number
    supervisor['phone_number'] = s.phone_number

    return supervisor


def _get_emergency_info(student_number):
    emergency = {}

    e = EmergencyContact.objects.get(student_number=student_number)

    emergency['emergency_name'] = e.emergency_name
    emergency['relation'] = e.relation
    emergency['phone_number'] = e.phone_number

    return emergency

# def add_student_info(request):
#     # add ALL student information
#     # return render(request, "add_student.html")
#
#     if request.method == "GET":
#         return render(request, "add_student.html")
#     else:
#         request.encoding = 'utf-8'
#         name = request.POST.get("name")
#         student_number = request.POST.get("student_number")
#         phone_number = request.POST.get("phone_number")
#
#         # if 'student_number' in request.GET and request.GET['student_number'] \
#         #         and 'name' in request.GET and request.GET['name'] \
#         #         and 'phone_number' in request.GET and request.GET['phone_number']:
#
#         with connection.cursor() as cur:
#             sql = "insert into dormsys_student(name,phone_number,student_number) values(%s,%s,%s);" \
#                   % ("'" + str(name) + "'", "'" + str(phone_number) + "'", "'" + str(student_number) + "'")
#             cur.execute(sql)
#             return HttpResponse("add student information successfully")
#
#
# def add_distribution_info(request):
#     # add ALL distribution information
#
#     if request.method == "GET":
#         return render(request, "add_distribution.html")
#     else:
#         request.encoding = 'utf-8'
#
#         student_number = request.POST.get("student_number")
#         room_number = request.POST.get("room_number")
#         region = request.POST.get("region")
#         apartment_number = request.POST.get("apartment_number")
#         with connection.cursor() as cur:
#             sql = "insert into dormsys_distribution(student_number,room_number,region,apartment_number) values(%s," \
#                   "%s,%s,%s);" % (
#                       "'" + str(student_number) + "'", "'" + str(room_number) + "'", "'" + str(region) + "'",
#                       "'" + str(apartment_number) + "'")
#             cur.execute(sql)
#
#         return HttpResponse("add distribution info successfully")
#
#
# def search_student_info(request):
#     # search student information by student number
#     if request.method == "GET":
#         return render(request, "search_student.html")
#     else:
#         request.encoding = 'utf-8'
#         student_number = request.POST.get("student_number")
#
#         with connection.cursor() as cur:
#             sql = "select * from dormsys_student where student_number=%s;" \
#                   % ("'" + str(student_number) + "'")
#             cur.execute(sql)
#             res = cur.fetchall()
#             # all_student = []
#             # for i in res:
#             #     tmp = {'name':i[1],'phone_number':i[2],'student_number':i[3]}
#             #     all_student.append(tmp)
#
#     return render(request, "someone_table.html", {'all_student': res})
#
#
# def delete_student_info(request):
#     # delete student information by student number
#
#     if request.method == "GET":
#         return render(request, "delete_student.html")
#     else:
#
#         request.encoding = 'utf-8'
#         student_number = request.POST.get("student_number")
#         with connection.cursor() as cur:
#             sql = "delete from dormsys_student where student_number=%s;" \
#                   % ("'" + str(student_number) + "'")
#             cur.execute(sql)
#
#     return HttpResponse("delete successfully")
#
#
# def update_student_info(request):
#     # update ALL other student information by student number
#
#     if request.method == "GET":
#         return render(request, "update_student.html")
#     else:
#         request.encoding = 'utf-8'
#         student_number = request.POST.get("student_number")
#         name = request.POST.get("name")
#         phone_number = request.POST.get("phone_number")
#
#         with connection.cursor() as cur:
#             sql = "UPDATE dormsys_student SET phone_number=%s,name=%s where student_number=%s;" \
#                   % ("'" + str(phone_number) + "'", "'" + str(name) + "'", "'" + str(student_number) + "'")
#             cur.execute(sql)
#
#     return HttpResponse("update successfully")
#
#
# def search_all_student(request):
#     if request.method == "GET":
#
#         request.encoding = 'utf-8'
#         student_number = request.POST.get("student_number")
#
#         with connection.cursor() as cur:
#             sql = "select * from dormsys_student;"
#             cur.execute(sql)
#             res = cur.fetchall()
#             # all_student = []
#             # for i in res:
#             #     tmp = {'name': i[1], 'phone_number': i[2], 'student_number': i[3]}
#             #     all_student.append(tmp)
#
#         return render(request, "student_table.html", {'all_student': res})
#     else:
#         return HttpResponse("error")
#
#

#
#
# def add_dorm_info(request):
#     # add ALL distribution information
#
#     if request.method == "GET":
#         return render(request, "add_dorm.html")
#     else:
#         request.encoding = 'utf-8'
#
#         room_number = request.POST.get("room_number")
#         region = request.POST.get("region")
#         apartment_number = request.POST.get("apartment_number")
#         story = request.POST.get("story")
#         with connection.cursor() as cur:
#             sql = "insert into dormsys_dorm(room_number,region,apartment_number,story) values(%s," \
#                   "%s,%s,%s);" % (
#                       "'" + str(room_number) + "'", "'" + str(region) + "'", "'" + str(apartment_number) + "'",
#                       "'" + str(story) + "'")
#             cur.execute(sql)
#
#         return HttpResponse("add dorm information successfully")
#
#
# def add_apartment_info(request):
#     # add ALL distribution information
#
#     if request.method == "GET":
#         return render(request, "add_apartment.html")
#     else:
#         request.encoding = 'utf-8'
#
#         region = request.POST.get("region")
#         apartment_number = request.POST.get("apartment_number")
#         with connection.cursor() as cur:
#             sql = "insert into dormsys_apartment(region,apartment_number) values(%s," \
#                   "%s);" % (
#                       "'" + str(region) + "'","'" + str(apartment_number) + "'")
#             cur.execute(sql)
#
#         return HttpResponse("add apartment information successfully")
