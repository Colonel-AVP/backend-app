from django.shortcuts import render
from rest_framework import generics
from .models import Department, Student, Subject, Staff, PNWebPushConfig
from .serializers import (
    DepartmentSerializer,
    StudentListSerializer,
    SubjectSerializer,
    StaffSerializer,
    FilteredStudentSerializer,
    StudentCreateSerializer,
    StaffCreateSerializer,
    PNWebPushConfigSerializer,
)
import urllib
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import serializers
import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from .tasks import get_department_count, department_exist_check, send_welcome_email
from celery.result import AsyncResult
from celery import group, chord, chain
from .tasks import add, multiply, subtract
from rest_framework.decorators import api_view
import requests

FACEBOOK_APP_ID = 643345242702738
REDIRECT_URL = "https://127.0.0.1:8000/api/login_redirect/"
APP_SECRET = "898c7633feba36e38b3cede59e9ea651"
CONFIG_ID = "300204523065054"

"""
https://www.facebook.com/v14.0/dialog/oauth?app_id=643345242702738&auth_type=&cbt=1707135878382&channel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df03ec88417e91a13d%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Fff016f1c06d5db74f%26relation%3Dopener&client_id=643345242702738&config_id=300204523065054&display=popup&domain=127.0.0.1&e2e=%7B%7D&fallback_redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Flogin%2F&force_confirmation=false&id=f4d59f9f0d831c7b5&locale=en_US&logger_id=74693b30-3193-46a0-9bd7-ef54636aece7&messenger_page_id=&origin=1&plugin_prepare=true&redirect_uri=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df4bcb634689d0c6ff%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Fff016f1c06d5db74f%26relation%3Dopener.parent%26frame%3Df4d59f9f0d831c7b5&ref=LoginButton&reset_messenger_state=false&response_type=signed_request%2Ctoken%2Cgraph_domain&scope=public_profile%2Cemail&sdk=joey&size=%7B%22width%22%3A600%2C%22height%22%3A679%7D&url=dialog%2Foauth&version=v14.0

"""


from django.http import HttpResponse


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        print(f"serializer --> {serializer.data}")
        name = serializer.validated_data.get("name")
        if department_exist_check(name):
            raise serializers.ValidationError(
                f"Department with name '{name}' already exists."
            )
        email_list = [serializer.validated_data.get("email")]
        send_welcome_email.delay(email_list)
        serializer.save()

    def get(self, request, *args, **kwargs):
        result = get_department_count.delay()
        # department_count = result.get()
        departments = self.get_queryset()
        serializer = self.get_serializer(departments, many=True)
        response_data = {
            # "department_count": department_count,
            "departments": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentCountView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        department_count = self.get_queryset().count()
        return Response(
            {"Total Departments:": department_count}, status=status.HTTP_200_OK
        )


class StudentListCreateView(generics.ListCreateAPIView):
    filter_backends = [SearchFilter]
    search_fields = ["name", "department__name"]
    queryset = Student.objects.all()

    def get_serializer_class(self):
        # Use different serializers based on the HTTP method
        if self.request.method == "POST":
            return StudentCreateSerializer
        else:
            return StudentListSerializer

    # def create(self, request, *args, **kwargs):
    #     extra_data = request.data.get("extra_data", {})
    #     extra_data_json = json.dumps(extra_data)
    #     student_data = request.data
    #     student_data["extra_data"] = extra_data_json
    #     print(f" student_data -> {student_data}")
    #     serializer = StudentCreateSerializer(data=student_data)
    #     print(f"serializer: {serializer}")
    #     # Validate the data
    #     if serializer.is_valid():
    #         student = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name", None)
        print(f"name --> {name}")
        department_name = self.request.query_params.get("department_name", None)
        print(f"department_name --> {department_name}")

        # Print queryset before applying filter
        print("Before Filter:", queryset)

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )  # Use case-insensitive search
        elif department_name:
            queryset = queryset.filter(department__name__icontains=department_name)

        return queryset

    # def get_serializer_class(self):
    #     # Choose the appropriate serializer based on the existence of query parameters
    #     if (
    #         "department_name" in self.request.query_params
    #         or "name" in self.request.query_params
    #     ):
    #         return FilteredStudentSerializer
    #     else:
    #         return StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer


class StudentCountView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

    def get(self, request, *args, **kwargs):
        student_count = self.get_queryset().count()
        return Response({"Total Students:": student_count}, status=status.HTTP_200_OK)


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectCountView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        subject_count = self.get_queryset().count()
        return Response({"Total Subject:": subject_count}, status=status.HTTP_200_OK)


class StaffListCreateView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    search_fields = ["name", "departments__name", "subjects__name"]

    def get_serializer_class(self):
        # Use different serializers based on the HTTP method
        if self.request.method == "POST":
            return StaffCreateSerializer
        else:
            return StaffSerializer

    # def perform_create(self, serializer):
    #     print(f"serializer --> {serializer.data}")

    #     email = serializer.validated_data.get("email")
    #     is_staff = Staff.objects.filter(email__iexact=email).exists()
    #     if is_staff:
    #         raise serializers.ValidationError(
    #             f"Staff with email '{email}' already exists."
    #         )
    #     send_welcome_email.delay(email)
    #     response = f"Staff Created Successfully {serializer.data})"
    #     serializer.save()
    #     return Response(response, status=status.HTTP_201_CREATED)


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffCountView(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get(self, request, *args, **kwargs):
        staff_count = self.get_queryset().count()
        return Response({"Total Staff:": staff_count}, status=status.HTTP_200_OK)


class PNWebPushConfigListCreateView(generics.ListCreateAPIView):
    queryset = PNWebPushConfig.objects.all()
    serializer_class = PNWebPushConfigSerializer


class PNWebPushConfigDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PNWebPushConfig.objects.all()
    serializer_class = PNWebPushConfigSerializer


@api_view(["GET"])
def perform_operations(request):
    # Assume x, y, and z are provided as query parameters
    x = int(request.GET.get("x", 0))
    y = int(request.GET.get("y", 0))
    z = int(request.GET.get("z", 0))

    header_group = group(add.s(x, y), add.s(y, z), add.s(x, z))
    print(header_group)
    print(type(header_group))
    # Create a chord with the header group and a callback task (body)
    result = chord(header_group)(subtract.s(5))
    print(result)
    # Execute the chord
    final_result = result.get()

    return Response(final_result, status=status.HTTP_200_OK)


@api_view(["GET"])
def facebook_login(request):
    """
    Facebook login page
    """

    login_url = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={REDIRECT_URL}&state=bfc&config_id=300204523065054"

    url = "https://www.facebook.com/v19.0/dialog/oauth?client_id=643345242702738&redirect_uri=20c1-49-207-216-135.ngrok-free.app&state=bfc"

    # response = requests.get(login_url)
    # print(response.content())
    return HttpResponseRedirect(url)


@api_view(["GET"])
def callback(request):
    # Handle the Facebook callback and exchange the code for an access token

    code = request.args.get("code")
    print(code)
    # token_url = f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&redirect_uri={REDIRECT_URL}&client_secret={APP_SECRET}&code={code}"
    # response = requests.get(token_url)
    # access_token = response.json().get("access_token")

    # Redirect to your app with the access token
    return Response(code, status=status.HTTP_200_OK)


def login_view(request):
    return render(request, "login.html")


@api_view(["GET"])
def check_permission(request):
    url = (
        "https://graph.facebook.com/v14.0/me/permissions&access_token="
        + "EAAJJHnyow5IBO7MZBcTVq3U4Ld64JGVBPXjplfWHcK2grZB0ZBoLrIYmj0eIOZAi0FY9YoJhjvNPng8XMo0zuUAo49HiiH2ZB04WCniZCQIZBSh84COvfkYqzjMZBDQF3HIEDrItuM8kTISuO65VAetQMJocVQIZCqzCSdIfXBYeRB9Lbc5zEM5qgfePYtS3DzhKIGkm687UK2QZDZD"
    )
    response = requests.get(url)
    return Response(response.json(), status=status.HTTP_200_OK)


"""
https://www.facebook.com/v14.0/dialog/oauth?app_id=643345242702738&auth_type&cbt=1707135736379&channel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df03ec88417e91a13d%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Fff016f1c06d5db74f%26relation%3Dopener&client_id=643345242702738&config_id&display=popup&domain=127.0.0.1&e2e=%7B%7D&fallback_redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Flogin%2F&force_confirmation=false&id=f4d59f9f0d831c7b5&locale=en_US&logger_id=74693b30-3193-46a0-9bd7-ef54636aece7&messenger_page_id&origin=1&plugin_prepare=true&redirect_uri=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df4bcb634689d0c6ff%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Fff016f1c06d5db74f%26relation%3Dopener.parent%26frame%3Df4d59f9f0d831c7b5&ref=LoginButton&reset_messenger_state=false&response_type=signed_request%2Ctoken%2Cgraph_domain&scope=public_profile%2Cemail&sdk=joey&size=%7B%22width%22%3A600%2C%22height%22%3A679%7D&url=dialog%2Foauth&version=v14.0&ret=login&fbapp_pres=0&tp=unspecified&ext=1707139345&hash=AeYrimI6w8c5jn1bu3w
"""
