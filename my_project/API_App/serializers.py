from rest_framework import serializers
from .models import (
    MstCompany, MstLocation, MstCategory, MstStandardActivity,
    MstRole, MstStatus, MstDepartment, MstUser,
    MstVerifier, MstUserRoleConfiguration
)

class MstCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = MstCompany
        fields = '__all__'
        read_only_fields = ('company_id',)
        extra_kwargs = {
            'is_active': {'required': True}
        }

class MstLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstLocation
        fields = '__all__'
        read_only_fields = ('location_id',)
        extra_kwargs = {
            'is_active': {'required': True}
        }

class MstCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MstCategory
        fields = ['category_id', 'category_name']
        read_only_fields = ('category_id',)
        extra_kwargs = {
            'category_name': {'required': True},
            'is_active': {'required': True}
        }

class MstStandardActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MstStandardActivity
        fields = ['sa_id', 'activity_name', 'category']
        read_only_fields = ('sa_id',)
        extra_kwargs = {
            'category': {'required': True},
            'activity_name': {'required': True},
            'is_active': {'required': True}
        }

class MstRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRole
        fields = '__all__'
        read_only_fields = ('role_id',)
        extra_kwargs = {
            'role_name': {'required': True},
            'is_active': {'required': True},
        }

class MstStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstStatus
        fields = '__all__'
        read_only_fields = ('status_id',)
        extra_kwargs = {
            'status_code': {'required': True},
            'status_name': {'required': True},
            'is_active': {'required': True}
        }

class MstDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstDepartment
        fields = '__all__'
        read_only_fields = ('department_id',)
        extra_kwargs = {
            'is_active': {'required': True}
        }

class MstUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstUser
        fields = '__all__'
        read_only_fields = ('user_id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'user_code': {'required': True},
            'email_id': {'required': True},
            'user_name': {'required': True},
            'is_active': {'required': True},
            'role': {'required': True}
        }

class MstVerifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstVerifier
        fields = '__all__'
        read_only_fields = ('map_dept_veri_id',)
        extra_kwargs = {
            'is_active': {'required': True}
        }

class MstUserRoleConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstUserRoleConfiguration
        fields = '__all__'
        read_only_fields = ('user_role_config_id',)
        extra_kwargs = {
            'user_code': {'required': True},
            'role_code': {'required': True},
            'is_active': {'required': True}
        }



# Serializer for login response
class LoginUserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    isHOD = serializers.SerializerMethodField()
    isVerifier = serializers.SerializerMethodField()
    locationId = serializers.IntegerField(source='location.location_id')
    departmentId = serializers.IntegerField(source='department.department_id', default=0)
    deptName = serializers.CharField(source='department.department_name')

    class Meta:
        model = MstUser
        fields = [
            'user_id', 'user_name', 'user_code', 'email_id', 'locationId', 'departmentId',
            'deptName', 'isAdmin', 'isHOD', 'isVerifier'
        ]

    def get_isAdmin(self, obj):
        # Check if the user's role name is 'Admin' (case-insensitive)
        if obj.role and hasattr(obj.role, 'role_name'):
            return 1 if obj.role.role_name.lower() == 'admin' else 0
        return 0

    def get_isHOD(self, obj):
        # Check if this user is HOD of their department
        if obj.department and obj.department.HOD:
            return 1 if obj.department.HOD.user_id == obj.user_id else 0
        return 0

    def get_isVerifier(self, obj):
        # Check if this user is a verifier in user's location
        return 1 if MstVerifier.objects.filter(
            verifier_id=obj.user_id,
            location=obj.location,
            is_active=True
        ).exists() else 0


# Serializer for userlist response
class UserListSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source='department.department_id', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = MstUser
        fields = ['user_id', 'user_name', 'email_id', 'department_id', 'department_name', 'user_role']

    def get_user_role(self, obj):
        # Check if this user is an HOD
        is_hod = MstDepartment.objects.filter(HOD=obj).exists()
        return "HOD" if is_hod else "EMPLOYEE"


# Serializer for verifierlist response
class VerifierListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = MstUser
        fields = ['user_id', 'user_name', 'email_id', 'department_name', 'user_role']

    def get_user_role(self, obj):
        return "VERIFIER"
    

# Serializer for add trn_activity  
from .models import TrnActivity

class TrnActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrnActivity
        fields = [
            'category',
            'ActivityName',
            'assign_to',
            'AssignedUserRole',
            'verifier',
            'TargetDate',
            'created_by',
            'CreatedOn',
            'status',
            'department',
            'AdditionalNote',
        ]


# Serializer for TrnActivityList Responce 
class TrnActivityListSerializer(serializers.ModelSerializer):
    Category = serializers.CharField(source='category.category_name', read_only=True)
    AssignedUser = serializers.CharField(source='assign_to.user_name', read_only=True)
    Verifier = serializers.CharField(source='verifier.user_name', read_only=True)
    CreatedBy = serializers.CharField(source='created_by.user_name', read_only=True)
    Department = serializers.CharField(source='department.department_name', read_only=True)
    Status = serializers.CharField(source='status.status_name', read_only=True)

    class Meta:
        model = TrnActivity
        fields = [
            'ActivityId',
            'ActivityName',
            'Category',
            'AssignedUser',
            'AssignedUserRole',
            'Verifier',
            'CreatedBy',
            'TargetDate',
            'CreatedOn',
            'Department',
            'Status',
            'Acceptance',
            'AdditionalNote',
        ]


# Serializer for Assigned Activity List Responce 
class AssignedActivitySerializer(serializers.ModelSerializer):
    Category = serializers.CharField(source='category.category_name', read_only=True)
    Verifier = serializers.CharField(source='verifier.user_name', read_only=True)
    CreatedBy = serializers.CharField(source='created_by.user_name', read_only=True)

    class Meta:
        model = TrnActivity
        fields = [
            'ActivityId',
            'ActivityName',
            'Category',
            'Verifier',
            'CreatedBy',
            'CreatedOn',
            'TargetDate',
            'AdditionalNote',
        ]



# Serializer for update trn_activity  
class TrnActivityAcceptanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrnActivity
        fields = ['Acceptance', 'modified_by', 'ModifiedOn', 'status', 'Comments']



# Serializer for add trn_activity_task  
from .models import TrnActivityTask

class TrnActivityTaskSerializer(serializers.ModelSerializer):
    IsPrimary = serializers.BooleanField(required=False, default=True)
    reference_task = serializers.PrimaryKeyRelatedField(
        queryset=TrnActivityTask.objects.all(),
        required=False,
        allow_null=True,
        default=None
    )

    class Meta:
        model = TrnActivityTask
        fields = '__all__'



# Serializer for Assigned Task List Responce 
class AssignedTaskSerializer(serializers.ModelSerializer):
    ActivityId = serializers.CharField(source='activity.ActivityId', read_only=True)
    Verifier = serializers.CharField(source='activity.verifier.user_name', read_only=True)
    Status = serializers.CharField(source='status.status_name', read_only=True)
    CreatedBy = serializers.SerializerMethodField()

    class Meta:
        model = TrnActivityTask
        fields = [
            'TaskId',
            'ActivityId',
            'TaskDescription',
            'AssignedOn',
            'Remarks',
            'TargetDate',
            'Status',
            'Verifier',
            'CreatedBy',
        ]

    def get_CreatedBy(self, obj):
        if not obj.IsPrimary:
            return obj.reference_task.assigned_to.user_name if obj.reference_task and obj.reference_task.assigned_to else None
        else:
            return obj.activity.created_by.user_name if obj.activity and obj.activity.created_by else None



# Serializer for add trn_task_update  
from .models import TrnTaskUpdate

class TrnTaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnTaskUpdate
        fields = '__all__'




from rest_framework import serializers
from .models import TrnActivityTask, TrnTaskUpdate

class VerifyActivitySerializer(serializers.ModelSerializer):
    CategoryName = serializers.CharField(source='activity.category.category_name', read_only=True)
    ActivityId = serializers.CharField(source='activity.ActivityId', read_only=True)
    ActivityName = serializers.CharField(source='activity.ActivityName', read_only=True)
    Description = serializers.CharField(source='activity.AdditionalNote', read_only=True)
    CreatedOn = serializers.DateTimeField(source='activity.CreatedOn', read_only=True)
    Status = serializers.CharField(source='activity.status.status_name', read_only=True)
    task_status = serializers.CharField(source='status.status_name', read_only=True)
    AssignedBy = serializers.CharField(source='activity.created_by.user_name', read_only=True)
    AssignedTo = serializers.CharField(source='assigned_to.user_name', read_only=True)
    AssignedUserRole = serializers.CharField(source='activity.AssignedUserRole', read_only=True)
    AssignedUserDept = serializers.CharField(source='activity.department.department_name', read_only=True)

    # 🔽 Custom method field to include latest ActionOn
    LastActionOn = serializers.SerializerMethodField()

    class Meta:
        model = TrnActivityTask
        fields = [
            'ActivityId',
            'CategoryName',
            'ActivityName',
            'Description',
            'CreatedOn',
            'TargetDate',
            'Status',
            'task_status',
            'AssignedBy',
            'AssignedTo',
            'AssignedUserRole',
            'AssignedUserDept',
            'LastActionOn', 
        ]

    def get_LastActionOn(self, obj):
        # Get latest task update for this task
        latest_update = TrnTaskUpdate.objects.filter(task_id=obj).order_by('-ActionOn').first()
        if latest_update:
            return latest_update.ActionOn
        return None



# Serializer for add trn_activity_update
from .models import TrnActivityUpdate

class TrnActivityUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrnActivityUpdate
        fields = ['activity_id', 'ActionOn', 'action_by', 'action_status', 'Comments']

    def validate(self, data):
        status = data.get("action_status")
        comments = data.get("Comments")

        if status.status_name.lower() == 'returned' and not comments:
            raise serializers.ValidationError("Comments are required when status is Reject.")
        if status.status_name.lower() == 'verified' and comments:
            raise serializers.ValidationError("Comments should be empty when status is Verify.")
        return data

    def create(self, validated_data):
        # Save activity update record
        activity_update = super().create(validated_data)

        activity = validated_data['activity_id']
        action_status = validated_data['action_status']

        if action_status.status_name.lower() == 'verified':
            # Set primary task status to the same as action_status
            TrnActivityTask.objects.filter(activity=activity, IsPrimary=True).update(status=action_status)

            # Also update activity status to ID 5 (verified)
            activity.status_id = 5
            activity.save(update_fields=['status_id'])

        elif action_status.status_name.lower() == 'returned':
            # Set primary task status to status_id 10 (rejected)
            TrnActivityTask.objects.filter(activity=activity, IsPrimary=True).update(status_id=10)

            # Do not change activity.status

        return activity_update


# class TrnActivityUpdateCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TrnActivityUpdate
#         fields = ['activity_id', 'ActionOn', 'action_by', 'action_status', 'Comments']

#     def validate(self, data):
#         status = data.get("action_status")
#         comments = data.get("Comments")

#         if status.status_name.lower() == 'reject' and not comments:
#             raise serializers.ValidationError("Comments are required when status is Reject.")
#         if status.status_name.lower() == 'verify' and comments:
#             raise serializers.ValidationError("Comments should be empty when status is Verify.")
#         return data

#     def create(self, validated_data):
#         # Create the TrnActivityUpdate record
#         activity_update = super().create(validated_data)

#         # Update the status of the related TrnActivity
#         activity = validated_data['activity_id']
#         activity.status = validated_data['action_status']
#         activity.save(update_fields=['status'])

#         return activity_update

