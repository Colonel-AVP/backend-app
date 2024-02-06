# urls.py
from django.urls import path
from .views import (
    DepartmentListCreateView,
    DepartmentDetailView,
    DepartmentCountView,
    StudentListCreateView,
    StudentDetailView,
    StudentCountView,
    SubjectListCreateView,
    SubjectDetailView,
    SubjectCountView,
    StaffListCreateView,
    StaffDetailView,
    StudentCountView,
    PNWebPushConfigListCreateView,
    PNWebPushConfigDetailView,
    perform_operations,
    facebook_login,
    callback,
    login_view,
    check_permission,
)


urlpatterns = [
    path("login/", login_view, name="login"),
    # path("permissions/", check_permission, name="permission"),
    # path("login/", facebook_login, name="login"),
    # path("login_redirect/", callback, name="callback"),
    path(
        "webpushconfig/",
        PNWebPushConfigListCreateView.as_view(),
        name="webpushconfig-list-create",
    ),
    path(
        "webpushconfig/<int:pk>/",
        PNWebPushConfigDetailView.as_view(),
        name="webpushconfig-update-delete",
    ),
    path(
        "departments/",
        DepartmentListCreateView.as_view(),
        name="department-list-create",
    ),
    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "departments/count/",
        DepartmentCountView.as_view(),
        name="department-count",
    ),
    # path(
    #     "departments/",
    #     Depar  DepartmentCountView
    # )
    path("students/", StudentListCreateView.as_view(), name="student-list-create"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path(
        "students/count/",
        StudentCountView.as_view(),
        name="students-count",
    ),
    path("subjects/", SubjectListCreateView.as_view(), name="subject-list-create"),
    path("subjects/<int:pk>/", SubjectDetailView.as_view(), name="subject-detail"),
    path(
        "subjects/count/",
        SubjectCountView.as_view(),
        name="subjects-count",
    ),
    path("staff/", StaffListCreateView.as_view(), name="staff-list-create"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path(
        "staff/count/",
        StudentCountView.as_view(),
        name="staff-count",
    ),
    path("math/", perform_operations, name="math"),
]


"""
https://www.facebook.com/v14.0/dialog/oauth?app_id=643345242702738&auth_type=&cbt=1707199327049&channel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Dfceb3574a55027878%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Ffe2729ca4618a2572%26relation%3Dopener&client_id=643345242702738&config_id=&display=popup&domain=127.0.0.1&e2e=%7B%7D&fallback_redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Flogin%2F&force_confirmation=false&id=fdca2a36324051804&locale=en_US&logger_id=9e9b45d4-589a-4003-bb2e-007d333ca19f&messenger_page_id=&origin=1&plugin_prepare=true&redirect_uri=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df5e67cd7308dbb1d0%26domain%3D127.0.0.1%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252F127.0.0.1%253A8000%252Ffe2729ca4618a2572%26relation%3Dopener.parent%26frame%3Dfdca2a36324051804&ref=LoginButton&reset_messenger_state=false&response_type=signed_request%2Ctoken%2Cgraph_domain&scope=public_profile%2Cemail&sdk=joey&size=%7B%22width%22%3A600%2C%22height%22%3A679%7D&url=dialog%2Foauth&version=v14.0

"""
