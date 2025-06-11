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

    class Meta:
        model = MstUser
        fields = [
            'user_id', 'user_name', 'user_code', 'email_id', 'locationId', 'departmentId',
            'isAdmin', 'isHOD', 'isVerifier'
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
    Category = serializers.CharField(source='activity.category.category_name', read_only=True)
    Verifier = serializers.CharField(source='activity.verifier.user_name', read_only=True)
    CreatedBy = serializers.CharField(source='activity.created_by.user_name', read_only=True)
    Status = serializers.CharField(source='status.status_name', read_only=True)  # if you want readable status name

    class Meta:
        model = TrnActivityTask
        fields = [
            'TaskId',
            'Category',
            'TaskDescription',
            'AssignedOn',
            'Remarks',
            'TargetDate',
            'Status',
            'Verifier',
            'CreatedBy',
        ]


# Serializer for add trn_task_update  
from .models import TrnTaskUpdate

class TrnTaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnTaskUpdate
        fields = '__all__'
