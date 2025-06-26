from tokenize import TokenError
from .models import MstCompany, MstDepartment
from .serializers import MstCompanySerializer, VerifyActivitySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


from django.http import HttpResponse
from django.urls import reverse

def homepage(request):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Homepage</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">Available API Endpoints</h1>
            <ul class="list-group">
                <li class="list-group-item">
                    <a href="{reverse('login')}">Login API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('companies')}">Companies API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('logout')}">Logout API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('category-list')}">Category API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('activity-by-category', kwargs={'category_id': 2})}">Activity API (Category 2)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('user-list', kwargs={'location_id': 1})}">Get Users API (Location 1)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('verifier-list', kwargs={'location_id': 1})}">Get Verifiers API (Location 1)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('add-trnActivity')}">Add TrnActivity API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('trnActivities-list', kwargs={'admin_id': 43})}">Get TrnActivities API (Admin 43)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('assignedActivities-list', kwargs={'user_id': 45})}">Get AssignedActivities API (User 45)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('update-activity-acceptance', kwargs={'activity_id': 1})}">Update TrnActivity API (ActivityId 1)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('add-task')}">Add Task API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('tasks-list', kwargs={'user_id': 6})}">Get AssignedTasks API (User 6)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('add-task-update')}">Add TaskUpdate API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('get-verify-activities', kwargs={'user_id': 6})}">Get VerifierActivities API (User 6)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('add-activity-update')}">Add ActivityUpdate API</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('close-activity', kwargs={'activity_id': 8})}">Close TrnActivity API (ActivityId 8)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('activity-detail', kwargs={'activity_id': 43})}">Get ActivityInfo API (Demo test activity)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('task-detail', kwargs={'task_id': 41})}">Get TaskInfo API (Demo test activity)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('activity-dashboard', kwargs={'admin_id': 43})}">Get Activity-StatusCount API (Admin 43)</a>
                </li>
                <li class="list-group-item">
                    <a href="{reverse('task-dashboard', kwargs={'user_id': 45})}">Get Task-StatusCount API (Admin 45)</a>
                </li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# from rest_framework.decorators import  authentication_classes
# from .authentiction import CookieJWTAuthentication  # import custom auth

@api_view(['GET'])
# @authentication_classes([CookieJWTAuthentication])
# @permission_classes([IsAuthenticated])
def companyApi(request):
    companies = MstCompany.objects.all()
    serializer = MstCompanySerializer(companies, many=True)
    return Response({'success': True, 'data': serializer.data})




from rest_framework_simplejwt.tokens import RefreshToken
from .models import MstUser
from .serializers import LoginUserSerializer

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'success': False, 'message': 'Something is missing'}, status=400)

    try:
        user = MstUser.objects.select_related('location', 'department').get(user_alias=username, is_active=True)
    except MstUser.DoesNotExist:
        return Response({'success': False, 'message': 'User not found'}, status=404)

    if user.password != password:
        return Response({'success': False, 'message': 'Incorrect password'}, status=401)


    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)  # Proper access token for auth

    # ✅ Serialize user data
    serializer = LoginUserSerializer(user)

    # ✅ Prepare response
    response = Response({
        'success': True,
        'message': f'Welcome {username}',
        'user': serializer.data,
        'access_token': access_token,
        'refresh_token': str(refresh)  # You can omit this if you don’t need to refresh from client
    })
    
    return response




# import requests
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import MstUser
# from .serializers import LoginUserSerializer
# import logging

# logger = logging.getLogger(__name__)

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if not username or not password:
#         return Response({'success': False, 'message': 'Username or password missing'}, status=400)

#     ad_api_url = "http://172.24.240.11:100/LDAP/api/AuthAPI/IsAccountAuthorized"
#     try:
#         ad_response = requests.post(ad_api_url, json={
#             "username": username,
#             "password": password
#         })

#         logger.info(f"AD API Response Status: {ad_response.status_code}")
#         logger.info(f"AD API Response Body: {ad_response.text}")

#         ad_data = ad_response.json()

#         if ad_response.status_code != 200 or not ad_data.get("result", False):
#             return Response({'success': False, 'message': 'Invalid AD credentials'}, status=401)

#     except requests.exceptions.RequestException as e:
#         logger.exception("AD request failed")
#         return Response({'success': False, 'message': f'AD authentication failed: {str(e)}'}, status=500)

#     except ValueError as e:
#         logger.exception("Error parsing AD response JSON")
#         return Response({'success': False, 'message': 'Invalid AD response format'}, status=500)

#     try:
#         user = MstUser.objects.select_related('location', 'department').get(user_alias=username, is_active=True)
#     except MstUser.DoesNotExist:
#         return Response({'success': False, 'message': 'User not found in local database'}, status=404)
#     except Exception as e:
#         logger.exception("Unexpected DB error")
#         return Response({'success': False, 'message': f'Database error: {str(e)}'}, status=500)

#     try:
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         serializer = LoginUserSerializer(user)
#     except Exception as e:
#         logger.exception("Error during token generation or serialization")
#         return Response({'success': False, 'message': f'JWT error: {str(e)}'}, status=500)

#     return Response({
#         'success': True,
#         'message': f'Welcome {username}',
#         'user': serializer.data,
#         'access_token': access_token,
#         'refresh_token': str(refresh)
#     })



from rest_framework.views import APIView
from rest_framework.response import Response

# Backend token blacklisting on logout
class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        
        if not refresh_token:
            return Response(
                {"success": False, "message": "Refresh token is required"},
                status=400
            )
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'success': True, 'message': 'Logged out successfully'},
                status=200
            )
        except TokenError as e:
            return Response(
                {'success': False, 'message': str(e)},
                status=400
            )




from .models import MstCategory, MstStandardActivity
from .serializers import MstCategorySerializer, MstStandardActivitySerializer



@api_view(['GET'])
def category_list(request):
    categories = MstCategory.objects.filter(is_active=True)
    serializer = MstCategorySerializer(categories, many=True)
    return Response({
        "success": "true",
        "message": "Categories fetched successfully.",
        "categories": serializer.data
    })


@api_view(['GET'])
def activity_list_by_category(request, category_id):
    activities = MstStandardActivity.objects.filter(category_id=category_id, is_active=True)
    serializer = MstStandardActivitySerializer(activities, many=True)
    return Response({
        "success": "true",
        "message": "Activities fetched successfully.",
        "activities": serializer.data
    })


from .serializers import UserListSerializer
from django.db.models import Q

class UserListAPIView(APIView):
    def get(self, request, location_id):
        user_name = request.query_params.get('user_name')
        department_name = request.query_params.get('department_name')
        user_role = request.query_params.get('user_role', '').upper()

        hod_user_ids = MstDepartment.objects.filter(
            HOD__isnull=False
        ).values_list('HOD_id', flat=True).distinct()

        if user_role == "HOD":
            users = MstUser.objects.filter(
                is_active=True,
                location_id=location_id,
                user_id__in=hod_user_ids
            ).exclude(role__role_name__iexact='admin')

            if department_name:
                users = users.filter(department__department_name__icontains=department_name)

        elif user_role == "EMPLOYEE":
            if user_name:
                users = MstUser.objects.filter(
                    is_active=True,
                    location_id=location_id,
                    user_name__icontains=user_name
                ).exclude(
                    Q(role__role_name__iexact='admin') | Q(user_id__in=hod_user_ids)
                )

                if department_name:
                    users = users.filter(department__department_name__icontains=department_name)

            elif department_name:
                # users = users.filter(department__department_name__icontains=department_name)
                users = MstUser.objects.filter(
                    is_active=True,
                    location_id=location_id,
                    department__department_name__icontains=department_name
                ).exclude(
                    Q(role__role_name__iexact='admin') | Q(user_id__in=hod_user_ids)
                )

            else:
                users = MstUser.objects.none()  # No user_name → return empty queryset

        else:
            return Response({
                "success": "false",
                "message": "User Role missing",
            })

        serializer = UserListSerializer(users, many=True)
        return Response({
            "success": "true",
            "message": "Users fetched successfully.",
            "users": serializer.data
        })

# class UserListAPIView(APIView):
#     def get(self, request, location_id):
#         user_name = request.query_params.get('user_name')
#         department_name = request.query_params.get('department_name')
#         user_role = request.query_params.get('user_role')

#         # Base queryset: users by location and not 'admin'
#         users = MstUser.objects.filter(
#             is_active=True,
#             location_id=location_id
#         ).exclude(role__role_name__iexact='admin')

#         # Apply user_name filter
#         if user_name:
#             users = users.filter(user_name__icontains=user_name)

#         # Apply department_name filter
#         if department_name:
#             users = users.filter(department__department_name__icontains=department_name)

#         # Apply user_role filter: check if user is HOD of any department
#         if user_role:
#             user_ids_who_are_hods = MstDepartment.objects.filter(HOD__isnull=False).values_list('HOD_id', flat=True)
#             if user_role.upper() == "HOD":
#                 users = users.filter(user_id__in=user_ids_who_are_hods)
#             elif user_role.upper() == "EMPLOYEE":
#                 users = users.exclude(user_id__in=user_ids_who_are_hods)

#         serializer = UserListSerializer(users, many=True)
#         return Response({
#             "success": "true",
#             "message": "Users fetched successfully.",
#             "users": serializer.data
#         })
    


from .serializers import VerifierListSerializer
from .models import MstVerifier

class VerifierUserListAPIView(APIView):
    def get(self, request, location_id):
        verifier_user_ids = MstVerifier.objects.values_list('verifier_id', flat=True)
        users = MstUser.objects.filter(is_active=True, location_id=location_id, user_id__in=verifier_user_ids)
        serializer = VerifierListSerializer(users, many=True)
        return Response({
            "success": "true",
            "message": "Verifiers fetched successfully.",
            "verifiers": serializer.data
        })



from rest_framework import status
from .serializers import TrnActivitySerializer

class TrnActivityCreateView(APIView):
    def post(self, request):
        serializer = TrnActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "true", 'message': 'Activity Assigned Successfully.', 'data': serializer.data})
        return Response({"success": "false"} ,serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from .models import TrnActivity
from .serializers import TrnActivityListSerializer

# class TrnActivityListView(APIView):
#     def get(self, request, admin_id):
#         activities = TrnActivity.objects.filter(created_by=admin_id, status=3).order_by('-CreatedOn')
#         serializer = TrnActivityListSerializer(activities, many=True)
#         return Response({
#             "success": "true",
#             "message": "TrnActivities fetched successfully.",
#             "trnActivities": serializer.data
#         })



class TrnActivityListView(APIView):
    def get(self, request, admin_id):
        # Get optional query parameters
        activity_name = request.query_params.get('activity_name', None)
        status = request.query_params.get('status', '1')

        # Base queryset
        activities = TrnActivity.objects.filter(created_by=admin_id)

        # Apply filters
        if activity_name:
            activities = activities.filter(ActivityName__icontains=activity_name)

        if status:
            activities = activities.filter(status=status)

        # Order by created date
        activities = activities.order_by('-CreatedOn')

        # Serialize and return response
        serializer = TrnActivityListSerializer(activities, many=True)
        return Response({
            "success": True,
            "message": "TrnActivities fetched successfully.",
            "trnActivities": serializer.data
        })

    

from .serializers import AssignedActivitySerializer

# class AssignedActivityListView(APIView):
#     def get(self, request, user_id):
#         activities = TrnActivity.objects.filter(assign_to=user_id, status=1).order_by('-CreatedOn')
#         serializer = AssignedActivitySerializer(activities, many=True)
#         return Response({
#             "success": "true",
#             "message": "Assigned activities fetched successfully.",
#             "assignedActivities": serializer.data
#         })

class AssignedActivityListView(APIView):
    def get(self, request, user_id):
        try:
            user = MstUser.objects.get(user_id=user_id)
        except MstUser.DoesNotExist:
            return Response({
                "success": "false",
                "message": "User not found.",
                "assignedActivities": []
            })

        # Check if user is a HOD
        hod_department = MstDepartment.objects.filter(HOD=user).first()

        # Get optional query parameters
        activity_name = request.query_params.get('activity_name', None)
        status = request.query_params.get('status', '1')

        if hod_department:
            # User is HOD
            activities = TrnActivity.objects.filter(
                department=hod_department,
                AssignedUserRole__iexact='HOD',
                status_id=1
            ).order_by('-CreatedOn')
        else:
            # User is Employee
            activities = TrnActivity.objects.filter(
                assign_to=user,
                status_id=1
            ).order_by('-CreatedOn')

        if activity_name:
            activities = activities.filter(ActivityName__icontains=activity_name)

        if status:
            activities = activities.filter(status=status)

        serializer = AssignedActivitySerializer(activities, many=True)
        return Response({
            "success": "true",
            "message": "Assigned activities fetched successfully.",
            "assignedActivities": serializer.data
        })





from .models import TrnActivity, MstUser
from .serializers import TrnActivityAcceptanceUpdateSerializer

class UpdateActivityAcceptanceView(APIView):
    def put(self, request, activity_id):
        try:
            activity = TrnActivity.objects.get(ActivityId=activity_id)
        except TrnActivity.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

        acceptance = request.data.get("Acceptance")  # 🔁 MODIFIED (extracted for logic below)

        # 🔁 MODIFIED: conditional logic for status
        status_id = 3 if acceptance == "Yes" else 7

        data = {
            "Acceptance": acceptance,  # 🔁 MODIFIED: use variable instead of inline call
            "modified_by": request.data.get("ActionBy"),  # 🔁 MODIFIED: renamed from request.data.get("modified_by")
            "status": status_id,  # 🔁 MODIFIED: dynamic status based on acceptance
            "ModifiedOn": request.data.get("ActionOn"),
            "Comments": request.data.get("Comments")  # Optional
        }

        serializer = TrnActivityAcceptanceUpdateSerializer(activity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Activity updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from .serializers import TrnActivityTaskSerializer

class TrnActivityTaskCreateView(APIView):
    def post(self, request):
        serializer = TrnActivityTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Task created successfully.",
                "tasks": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



from .models import TrnActivityTask
from .serializers import AssignedTaskSerializer

# class AssignedTaskListView(APIView):
#     def get(self, request, user_id):
#         tasks = TrnActivityTask.objects.filter(assigned_to__user_id=user_id).order_by('-AssignedOn')
#         serializer = AssignedTaskSerializer(tasks, many=True)
#         return Response({
#             "success": "true",
#             "message": "Tasks fetched successfully.",
#             "assignedTasks": serializer.data
#         })


# class AssignedTaskListView(APIView):
#     def get(self, request, user_id):
#         # Get optional query parameters
#         task_name = request.query_params.get('task_name', None)
#         status = request.query_params.get('status', '2')

#         # Base queryset
#         tasks = TrnActivityTask.objects.filter(assigned_to__user_id=user_id)

#         # Apply filters
#         if task_name:
#             tasks = tasks.filter(TaskDescription__icontains=task_name)

#         if status:
#             tasks = tasks.filter(status=status)

#         # Order by created date
#         tasks = tasks.order_by('-AssignedOn')
#         serializer = AssignedTaskSerializer(tasks, many=True)
#         return Response({
#             "success": "true",
#             "message": "Tasks fetched successfully.",
#             "assignedTasks": serializer.data
#         })
    
class AssignedTaskListView(APIView):
    def get(self, request, user_id):
        try:
            user = MstUser.objects.get(user_id=user_id)
        except MstUser.DoesNotExist:
            return Response({
                "success": "false",
                "message": "User not found.",
                "assignedActivities": []
            })

        # Check if user is a HOD
        hod_department = MstDepartment.objects.filter(HOD=user).first()

        # Get optional query parameters
        task_name = request.query_params.get('task_name', None)
        status = request.query_params.get('status', '2')

        if hod_department:
            # User is HOD
            tasks = TrnActivityTask.objects.filter(
                IsPrimary=1,
                activity__department=hod_department,
                activity__AssignedUserRole__iexact='HOD',
            )
        else:
            # User is Employee
            tasks = TrnActivityTask.objects.filter(assigned_to__user_id=user_id)      

        # Apply filters
        if task_name:
            tasks = tasks.filter(TaskDescription__icontains=task_name)

        if status:
            tasks = tasks.filter(status=status)

        # Order by created date
        tasks = tasks.order_by('-AssignedOn')
        serializer = AssignedTaskSerializer(tasks, many=True)
        return Response({
            "success": "true",
            "message": "Tasks fetched successfully.",
            "assignedTasks": serializer.data
        })



from .serializers import TrnTaskUpdateSerializer

# class TrnTaskUpdateCreateView(APIView):
#     def post(self, request):
#         serializer = TrnTaskUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Task Updated successfully.",
#                 "taskUpdates": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "success": False,
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

class TrnTaskUpdateCreateView(APIView):
    def post(self, request):
        serializer = TrnTaskUpdateSerializer(data=request.data)
        if serializer.is_valid():
            task_update = serializer.save()

            # Update the corresponding TrnActivityTask action_status
            task = task_update.task_id  # FK instance
            task.status = task_update.action_status
            task.save()

            return Response(
                {   
                    "success": True,
                    "message": "Task Updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.db.models import OuterRef, Subquery, DateTimeField
from .models import TrnTaskUpdate

class VerifyActivityListView(APIView):
    def get(self, request, user_id):
        # Subquery to get latest ActionOn per task
        latest_actionon_subquery = TrnTaskUpdate.objects.filter(
            task_id=OuterRef('pk')
        ).order_by('-ActionOn').values('ActionOn')[:1]

        # Annotate each task with latest ActionOn and order by it
        activities = TrnActivityTask.objects.select_related('activity').annotate(
            last_actionon=Subquery(latest_actionon_subquery, output_field=DateTimeField())
        ).filter(
            IsPrimary=True,
            activity__status__in=[3, 5],
            activity__verifier__user_id=user_id,
            status__in=[5, 8]
        ).order_by('-last_actionon')  # ⬅️ Order by latest action

        serializer = VerifyActivitySerializer(activities, many=True)
        return Response(
            {
                "success": True,
                "message": "Verifier Activities Fetched successfully.",
                "activities": serializer.data
            },
            status=status.HTTP_200_OK
        )
    

from .serializers import TrnActivityUpdateCreateSerializer

class TrnActivityUpdateCreateView(APIView):
    def post(self, request):
        serializer = TrnActivityUpdateCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Activity Update Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from .serializers import TrnActivityCloseSerializer

class TrnActivityCloseAPIView(APIView):
    def put(self, request, activity_id):
        activity = TrnActivity.objects.get(ActivityId=activity_id)
        serializer = TrnActivityCloseSerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Activity Close Updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




from .serializers import ActivityDataSerializer

class ActivityDetailView(APIView):
    def get(self, request, activity_id):
        try:
            activity = TrnActivity.objects.get(ActivityId=activity_id)
        except TrnActivity.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivityDataSerializer(activity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from .serializers import TaskDetailSerializer

class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = TrnActivityTask.objects.get(TaskId=task_id)
        except TrnActivityTask.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



from rest_framework import status as drf_status
from django.db.models import Count
from datetime import date

from datetime import date
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.views import APIView
from django.db.models import Count

class ActivityDashboardAPIView(APIView):
    def get(self, request, admin_id):
        if not MstUser.objects.filter(user_id=admin_id, is_active=True).exists():
            return Response({"error": "Admin user not found."}, status=drf_status.HTTP_404_NOT_FOUND)

        today = date.today()
        activities = TrnActivity.objects.filter(created_by_id=admin_id)

        # Count by status
        status_counts = activities.values('status__status_name').annotate(
            count=Count('ActivityId')
        ).order_by('status__status_name')

        # Delayed activities (status_id 1 or 3 and target date < today)
        delayed_queryset = activities.filter(
            status__status_id__in=[1, 3],
            TargetDate__lt=today
        )

        delayed_data = []
        for activity in delayed_queryset:
            serialized = TrnActivityListSerializer(activity).data
            # Manually add DelayedDays
            delayed_days = (today - activity.TargetDate).days if activity.TargetDate else 0
            serialized['DelayedDays'] = delayed_days
            delayed_data.append(serialized)

        delayed_count = len(delayed_data)

        # OnTrack count
        onTrack_count = activities.filter(
            status__status_id=3,
            TargetDate__gte=today
        ).count()

        # Format result
        response_data = {
            "status_wise_counts": {
                entry['status__status_name']: entry['count'] for entry in status_counts
            },
            "delayed_activity_count": delayed_count,
            "onTrack_activity_count": onTrack_count,
            "delayed_activities": delayed_data  
        }

        return Response(response_data, status=drf_status.HTTP_200_OK)


from django.db.models import Count, Q

class UserDashboardAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = MstUser.objects.get(user_id=user_id)
        except MstUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        today = date.today()

        # Check if user is a HOD
        hod_department = MstDepartment.objects.filter(HOD=user).first()

        if hod_department:
            tasks = TrnActivityTask.objects.filter(
                IsPrimary=1,
                activity__department=hod_department,
                activity__AssignedUserRole__iexact="HOD",
            )
        else:
            tasks = TrnActivityTask.objects.filter(assigned_to__user_id=user_id)

        # Count by status
        status_counts = (
            tasks.values("status__status_name")
            .annotate(count=Count("TaskId"))
            .order_by("status__status_name")
        )

        # ✅ Delayed count (status_id 2, 10 or 3 and target date < today)
        delayed_count = tasks.filter(
            status__status_id__in=[2, 10, 3],
            TargetDate__lt=today
        ).count()

        # ✅ Format result
        response_data = {
            "status_wise_counts": {
                entry['status__status_name']: entry['count'] for entry in status_counts
            },
            "delayed_task_count": delayed_count,
        }

        return Response(response_data, status=status.HTTP_200_OK)



# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             username = body.get('username')
#             password = body.get('password')

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         user_id,
#                         user_alias,
#                         user_code,
#                         email_id,
#                         ISNULL(Mst_User.location_id, 0) AS location_id,
#                         ISNULL(Mst_User.department_id, 0) AS department_id,
#                         CASE 
#                             WHEN Mst_Department.department_id IS NULL THEN 0 
#                             ELSE 1 
#                         END AS IsHOD,
#                         CASE 
#                             WHEN Mst_Verifier.verifier_id IS NULL THEN 0 
#                             ELSE 1 
#                         END AS isVerifier
#                     FROM 
#                         Mst_User
#                     LEFT JOIN 
#                         Mst_Department 
#                         ON Mst_Department.department_id = Mst_User.department_id 
#                         AND Mst_Department.location_id = Mst_User.location_id
#                     LEFT JOIN 
#                         Mst_Verifier 
#                         ON Mst_Verifier.verifier_id = Mst_User.user_id 
#                         AND Mst_Verifier.location_id = Mst_User.location_id
#                     WHERE 
#                         user_name = %s
#                         AND password = %s
#                 """, [username, password])
#                 row = cursor.fetchone()

#             if row:
#                 # Map your columns here
#                 (
#                     userid,
#                     UserAlias,
#                     usercode,
#                     EmailID,
#                     locationid,
#                     DepartmentID,
#                     IsHOD,
#                     isVerifier
#                 ) = row

#                 return JsonResponse({
#                     'success': True,
#                     'userId': userid,
#                     'UserAlias': UserAlias,
#                     'userCode': usercode,
#                     'emailId': EmailID,
#                     'locationId': locationid,
#                     'departmentId': DepartmentID,
#                     'isHOD': IsHOD,
#                     'isVerifier': isVerifier,
#                 })
#             else:
#                 return JsonResponse({'success': False, 'message': 'Invalid username or password'})

#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'error': 'POST request required'}, status=400)



    

