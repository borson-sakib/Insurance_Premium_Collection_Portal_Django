from xmlrpc.client import DateTime
from django.db import models
from datetime import datetime, timezone
# from django.utils.timezone import datetime, now
import uuid

# from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

# [PolicyNO]
#            ,[ProposersName]
#            ,[ProposersAddress]
#            ,[Riskdate]
#            ,[sumassured]
#            ,[planno]
#            ,[Term]
#            ,[mode]
#            ,[TotalPremium]
#            ,[NextDueDate]
#            ,[NoOfInstalment]
#            ,[MobileNo]
#            ,[MaturityDate]
#            --,[EntryDate]
# 		   ,[DepositorsMobileNO]
# 		   ,[AmountToReceive]
#            ,[Inputter]
#            ,[BranchCode]
#            ,[InputterIP])

# now = timezone.now


class Branch (models.Model):
    branch_id = models.CharField(max_length=50, null=True)
    branch_code= models.CharField(max_length=200, null=True, unique=True)
    branch_name = models.CharField(max_length=200, null=False, unique=True)
    is_branch = models.BooleanField(default=True, null=True)
    branch_mnemonic = models.CharField(max_length=7, null=True)
    sbs_code = models.CharField(max_length=50, null=True)
    branch_address = models.CharField(max_length=450, null=True)
    created_by = models.CharField(max_length=450, null=True)
    creat_date = models.CharField(max_length=450, null=True)
    status = models.CharField(max_length=450, null=True)


    def getBranchObj(string):
        obj = self.objects.get(branch_name=string)
        return obj


class User(models.Model):
    
    
    email = models.EmailField( null=False)
    displayname = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, default='N/A', null=True)
    branchname = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    employeeID = models.CharField(max_length=20, null=True)
    is_admin = models.BooleanField(default=False)

    
    def displayName(self):
        return self.displayname

    def is_staff(self):
        if self.is_admin:
            return True
        else:
            return False





class Transaction(models.Model):
    # user_id = models.CharField(max_length=30)
    # user_pwd = models.CharField(max_length=30)
    policy_no = models.CharField(max_length=30)
    amount = models.FloatField(max_length=30)
    payermobile_no = models.CharField(max_length=30)
    # payformobile_no = models.CharField(max_length=30)
    remarks = models.CharField(max_length=1000,null=True)
    txn_id = models.CharField( max_length=30, editable=False,null=True)
    txn_date = models.DateTimeField(default=datetime.now(),null=True, editable=False)
    msg = models.CharField(max_length=30,default="S",editable=False)
    status = models.BooleanField(default=False)
    input_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
   

