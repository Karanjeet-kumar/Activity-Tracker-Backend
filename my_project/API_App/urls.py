from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from API_App import views
from .views import ActivityDashboardAPIView, ActivityDetailView, AssignedActivityListView, AssignedTaskListView, DepartmentListAPIView, LogoutAPIView, TaskDetailView, TrnActivityCloseAPIView, TrnActivityCreateView, TrnActivityListView, TrnActivityTaskCreateView, TrnActivityUpdateCreateView, TrnTaskUpdateCreateView, UpdateActivityAcceptanceView, UserDashboardAPIView, UserListAPIView, VerifierUserListAPIView, VerifyActivityListView

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.homepage, name='home'),  
    path('login/', views.login, name='login'),  
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('companies/', views.companyApi, name='companies'),
    path('get/categories/', views.category_list, name='category-list'),
    path('get/activities/<int:category_id>/', views.activity_list_by_category, name='activity-by-category'),
    path('get/departments/<int:location_id>/', DepartmentListAPIView.as_view(), name='dept-list'),
    path('get/users/<int:location_id>/', UserListAPIView.as_view(), name='user-list'),
    path('get/verifiers/<int:location_id>/', VerifierUserListAPIView.as_view(), name='verifier-list'),
    path('add/trnActivity/', TrnActivityCreateView.as_view(), name='add-trnActivity'),
    path('trnActivities/admin/<int:admin_id>/', TrnActivityListView.as_view(), name='trnActivities-list'),
    path('trnActivities/user/<int:user_id>/', AssignedActivityListView.as_view(), name='assignedActivities-list'),
    path('trnActivities/update/<int:activity_id>/', UpdateActivityAcceptanceView.as_view(), name='update-activity-acceptance'),
    path('add/task/', TrnActivityTaskCreateView.as_view(), name='add-task'),
    path('tasks/<int:user_id>/', AssignedTaskListView.as_view(), name='tasks-list'),
    path('add/task-updates/', TrnTaskUpdateCreateView.as_view(), name='add-task-update'),
    path('get/verifiers/activities/<int:user_id>/', VerifyActivityListView.as_view(), name='get-verify-activities'),
    path('add/activity-updates/', TrnActivityUpdateCreateView.as_view(), name='add-activity-update'),
    path('trnActivities/close/<int:activity_id>/', TrnActivityCloseAPIView.as_view(), name='close-activity'),
    path('activityInfo/<int:activity_id>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('taskInfo/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('dashboard-activity-status/<int:admin_id>/', ActivityDashboardAPIView.as_view(), name='activity-dashboard'),
    path('dashboard-task-status/<int:user_id>/', UserDashboardAPIView.as_view(), name='task-dashboard'),
]

