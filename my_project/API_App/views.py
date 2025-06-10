from tokenize import TokenError
from .models import MstCompany, MstDepartment
from .serializers import MstCompanySerializer
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
                    <a href="{reverse('trnActivities-list')}">Get TrnActivities API</a>
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
        user = MstUser.objects.select_related('location', 'department').get(user_name=username, is_active=True)
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


# from .serializers import UserListSerializer

# class UserListAPIView(APIView):
#     def get(self, request, location_id):
#         # Exclude users whose role name is 'admin'
#         users = MstUser.objects.filter(is_active=True, location_id=location_id).exclude(role__role_name__iexact='admin')

#         serializer = UserListSerializer(users, many=True)
#         return Response({
#             "success": "true",
#             "message": "Users fetched successfully.",
#             "users": serializer.data
#         })
    


from .serializers import UserListSerializer

class UserListAPIView(APIView):
    def get(self, request, location_id):
        user_name = request.query_params.get('user_name')
        department_name = request.query_params.get('department_name')
        user_role = request.query_params.get('user_role')

        # Base queryset: users by location and not 'admin'
        users = MstUser.objects.filter(
            is_active=True,
            location_id=location_id
        ).exclude(role__role_name__iexact='admin')

        # Apply user_name filter
        if user_name:
            users = users.filter(user_name__icontains=user_name)

        # Apply department_name filter
        if department_name:
            users = users.filter(department__department_name__icontains=department_name)

        # Apply user_role filter: check if user is HOD of any department
        if user_role:
            user_ids_who_are_hods = MstDepartment.objects.filter(HOD__isnull=False).values_list('HOD_id', flat=True)
            if user_role.upper() == "HOD":
                users = users.filter(user_id__in=user_ids_who_are_hods)
            elif user_role.upper() == "EMPLOYEE":
                users = users.exclude(user_id__in=user_ids_who_are_hods)

        serializer = UserListSerializer(users, many=True)
        return Response({
            "success": "true",
            "message": "Users fetched successfully.",
            "users": serializer.data
        })
    


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

class TrnActivityListView(APIView):
    def get(self, request):
        activities = TrnActivity.objects.all().order_by('-CreatedOn')
        serializer = TrnActivityListSerializer(activities, many=True)
        return Response({
            "success": "true",
            "message": "TrnActivities fetched successfully.",
            "trnActivities": serializer.data
        })
    

from .serializers import AssignedActivitySerializer

class AssignedActivityListView(APIView):
    def get(self, request, user_id):
        tasks = TrnActivity.objects.filter(assign_to=user_id, status=1).order_by('-CreatedOn')
        serializer = AssignedActivitySerializer(tasks, many=True)
        return Response({
            "success": "true",
            "message": "Assigned activities fetched successfully.",
            "assignedActivities": serializer.data
        })




from django.utils import timezone
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
        status_id = 2 if acceptance == "Yes" else 7

        data = {
            "Acceptance": acceptance,  # 🔁 MODIFIED: use variable instead of inline call
            "modified_by": request.data.get("ActionBy"),  # 🔁 MODIFIED: renamed from request.data.get("modified_by")
            "status": status_id,  # 🔁 MODIFIED: dynamic status based on acceptance
            "ModifiedOn": timezone.now(),
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

class AssignedTaskListView(APIView):
    def get(self, request, user_id):
        tasks = TrnActivityTask.objects.filter(assigned_to__user_id=user_id)
        serializer = AssignedTaskSerializer(tasks, many=True)
        return Response({
            "success": "true",
            "message": "Tasks fetched successfully.",
            "assignedTasks": serializer.data
        })





# Without using serializer-----------------------

# from django.utils import timezone
# from .models import TrnActivity, MstUser

# class UpdateActivityAcceptanceView(APIView):
#     def put(self, request, ActivityId):
#         try:
#             activity = TrnActivity.objects.get(ActivityId=ActivityId)
#         except TrnActivity.DoesNotExist:
#             return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

#         acceptance = request.data.get("Acceptance")
#         modified_by_id = request.data.get("modified_by")

#         try:
#             modified_by = MstUser.objects.get(user_id=modified_by_id)
#         except MstUser.DoesNotExist:
#             return Response({"error": "Modifier user not found."}, status=status.HTTP_400_BAD_REQUEST)

#         activity.Acceptance = acceptance
#         activity.modified_by = modified_by
#         activity.ModifiedOn = timezone.now()
#         activity.save()

#         return Response({
#             "success": True,
#             "message": "Activity acceptance updated successfully.",
#             "ActivityId": activity.ActivityId,
#             "Acceptance": activity.Acceptance,
#             "ModifiedBy": activity.modified_by.user_name,
#             "ModifiedOn": activity.ModifiedOn,
#         }, status=status.HTTP_200_OK)



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



    

