from django.urls import path
from .views import (
    IndexView, LoginView, PanelView, MemberListView,
    HomeView, LogoutView, UnicodeView, DeleteMemberView,
    GradeManageView,
)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('index', IndexView.as_view(), name='admin_index'),
    path('login', LoginView.as_view(), name='admin_login'),
    path('panel', PanelView.as_view(), name='admin_panel'),
    path('member/list', MemberListView.as_view(), name='member_list'),
    path('home', HomeView.as_view(), name='admin_home'),
    path('logout', LogoutView.as_view(), name='admin_logout'),
    path('unicode', UnicodeView.as_view(), name='admin_unicode'),
    path('grademanage', GradeManageView.as_view(), name='admin_grade_manage'),
    path('deletemember', DeleteMemberView.as_view(), name='admin_delete_member'),
]
