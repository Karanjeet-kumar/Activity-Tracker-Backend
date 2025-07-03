from django.db import models


# Create your models here.
class MstCompany(models.Model):
    company_id = models.AutoField(primary_key=True)  
    company_name = models.CharField(max_length=250, null=True, blank=True)
    company_code = models.CharField(max_length=5, null=True, blank=True)
    company_abbreviation = models.CharField(max_length=10, null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.IntegerField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField()

    class Meta:
        db_table = 'Mst_Company'

class MstLocation(models.Model):
    location_id = models.AutoField(primary_key=True)  
    location_name = models.CharField(max_length=250, null=True, blank=True)
    company = models.ForeignKey(MstCompany, on_delete=models.SET_NULL, null=True, db_column='company_id')
    created_by = models.IntegerField(null=True, blank=True)  
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.IntegerField(null=True, blank=True) 
    modified_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField()

    class Meta:
        db_table = 'Mst_Location'

class MstCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Mst_Category'

class MstStandardActivity(models.Model):
    sa_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(MstCategory, on_delete=models.CASCADE, db_column='category_id')
    activity_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Mst_StandardActivity'

class MstRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    deactive_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Mst_Role'

class MstStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_code = models.CharField(max_length=20)
    status_name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    deactive_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Mst_Status'

class MstDepartment(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(MstLocation, on_delete=models.SET_NULL, null=True, db_column='location_id')
    HOD = models.ForeignKey('MstUser', on_delete=models.SET_NULL, null=True, db_column='hod')
    created_by = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.IntegerField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField()

    class Meta:
        db_table = 'Mst_Department'

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MstUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError("The user_name must be set")
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(user_name, password, **extra_fields)

class MstUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_code = models.CharField(max_length=10)
    email_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100, unique=True)  # must be unique for auth
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    role = models.ForeignKey(MstRole, on_delete=models.CASCADE, db_column='role_id')
    user_alias = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(MstLocation, on_delete=models.CASCADE, db_column='location_id')
    department = models.ForeignKey(MstDepartment, on_delete=models.SET_NULL, null=True, db_column='department_id')

    objects = MstUserManager()

    USERNAME_FIELD = 'user_name'  # Django will use this to log in

    class Meta:
        db_table = 'Mst_User'

    @property
    def id(self):
        return self.user_id
    

class MstVerifier(models.Model):
    map_dept_veri_id = models.AutoField(primary_key=True)
    department_id = models.IntegerField(null=True, blank=True)
    verifier_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=255,null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(MstLocation,on_delete=models.SET_NULL, null=True, db_column='location_id')

    class Meta:
        db_table = 'Mst_Verifier'

class MstUserRoleConfiguration(models.Model):
    user_role_config_id = models.AutoField(primary_key=True)
    user_code = models.CharField(max_length=10)
    role_code = models.CharField(max_length=10)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Mst_UserRoleConfiguration'
        unique_together = (('user_code', 'role_code'),)



# Required Transacttion Table Model

class TrnActivity(models.Model):
    ActivityId = models.AutoField(primary_key=True)
    category = models.ForeignKey(MstCategory, on_delete=models.CASCADE, db_column='CategoryId')
    ActivityName = models.CharField(max_length=100)
    
    verifier = models.ForeignKey(
        MstUser, 
        on_delete=models.SET_NULL, null=True,
        db_column='VerifierId', 
        related_name='activities_verified'
    )
    assign_to = models.ForeignKey(
        MstUser, 
        on_delete=models.CASCADE, 
        db_column='AssignedUserId', 
        related_name='activities_assigned'
    )
    
    status = models.ForeignKey(MstStatus, on_delete=models.CASCADE, db_column='StatusId')
    AssignedUserRole =  models.CharField(max_length=100)
    TargetDate = models.DateField()
    department = models.ForeignKey(MstDepartment, on_delete=models.CASCADE, db_column='DepartmentId')
    CreatedOn = models.DateTimeField()
    ClosedOn = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey(
        MstUser, 
        on_delete=models.CASCADE, 
        db_column='CreatedBy', 
        related_name='activities_created'
    )
    ModifiedOn = models.DateTimeField(null=True, blank=True)
    
    modified_by = models.ForeignKey(
        MstUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='ModifiedBy', 
        related_name='activities_modified'
    )
    Acceptance = models.CharField(max_length=5, null=True, blank=True)
    AdditionalNote = models.TextField(null=True, blank=True)
    Comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Trn_Activity'


class TrnActivityTask(models.Model):
    TaskId = models.AutoField(primary_key=True) 
    TaskDescription = models.TextField()

    assigned_to = models.ForeignKey(
        MstUser,
        on_delete=models.CASCADE,
        db_column='AssignedTo'
    )
    AssignedOn = models.DateTimeField()
    TargetDate = models.DateField()

    status = models.ForeignKey(
        MstStatus,
        on_delete=models.CASCADE,
        db_column='StatusId'
    )

    activity = models.ForeignKey(
        TrnActivity,
        on_delete=models.CASCADE,
        db_column='ActivityID'
    )

    IsPrimary = models.BooleanField(default=True)

    reference_task = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ReferenceTaskID'
    )

    Remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Trn_Activity_Task'


class TrnTaskUpdate(models.Model):
    UpdateId = models.AutoField(primary_key=True) 

    task_id = models.ForeignKey(
        TrnActivityTask,
        on_delete=models.CASCADE,
        db_column='TaskId'
    )

    action_by = models.ForeignKey(
        MstUser, 
        on_delete=models.CASCADE,
        db_column='ActionBy', 
    )

    ActionOn = models.DateTimeField()

    action_status = models.ForeignKey(
        MstStatus,
        on_delete=models.CASCADE,
        db_column='ActionStatus'
    )

    Remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Trn_Task_Update'


        
class TrnActivityUpdate(models.Model):
    ActUpdateId = models.AutoField(primary_key=True) 

    activity_id = models.ForeignKey(
        TrnActivity,
        on_delete=models.CASCADE,
        db_column='ActivityId'
    )

    action_by = models.ForeignKey(
        MstUser, 
        on_delete=models.CASCADE,
        db_column='ActionBy', 
    )

    ActionOn = models.DateTimeField()

    action_status = models.ForeignKey(
        MstStatus,
        on_delete=models.CASCADE,
        db_column='ActionStatus'
    )

    Comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Trn_Activity_Update'


