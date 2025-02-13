from .models import User, ExpenseCategory, ExpenseClaim
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS
# password related imports
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
# password related imports
# from django.db.models import Sum

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','role','password','supervisor','is_active','date_joined']
    
    @staticmethod
    def pw_validate_and_hash(raw_pw):
        # check password validation
        try:
            validate_password(raw_pw)
        except Exception as e:
            raise serializers.ValidationError({'password': e})
        # hash password
        hashedpw = make_password(raw_pw)
        return hashedpw
        
    def get_fields(self):
        a = super().get_fields()
        if self.context.get('request').method in ['PUT','PATCH'] and not self.context.get('request').user.is_admin:
            fields_to_pop = ['date_joined', 'supervisor', 'is_active', 'role']
            [a.pop(x) for x in fields_to_pop]
        return a
    
    def to_representation(self, instance):
        a = super().to_representation(instance)
        if a['supervisor']:
            a['supervisor'] = instance.supervisor.username
        for key, val in a.items():
            if val == None or val == '':
                a[key] = 'N/A'
        return a
    
    def create(self, validated_data):
        # get password
        pw = validated_data.get('password')
        passwd = self.pw_validate_and_hash(pw)
        # update password and save in db
        validated_data['password'] = passwd
        validated_data['is_active'] = True
        instance = User(**validated_data)
        try:
            instance.full_clean()
        except Exception as e:
            raise serializers.ValidationError(e)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        a = super().update(instance, validated_data)
        if 'password' in validated_data:
            passwd = self.pw_validate_and_hash(validated_data['password'])
            instance.password = passwd
        try:
            instance.full_clean()
        except Exception as e:
            raise serializers.ValidationError(e)
        instance.save()
        return a
        
class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
        
        
class ExpenseClaimSerializer(serializers.ModelSerializer):
    # employee_detail = UserSerializer(source='employee')
    # level = serializers.CharField(source='status')
    # my_total_claims = serializers.SerializerMethodField()
    class Meta:
        model = ExpenseClaim
        fields = '__all__'
        
    # def get_my_total_claims(self, obj):
    #     id = obj.employee.pk
    #     instance = User.objects.get(pk = id)
    #     allclaims = instance.empallclaims.all()
    #     totalval = allclaims.aggregate(totalclaims=Sum('amount'))
    #     return totalval['totalclaims']
        
    def get_fields(self):
        fd = super().get_fields()
        request = self.context.get('request')
        if request.user.is_authenticated and not request.user.is_admin:
            fd.pop('employee')
            # fd['employee'].read_only = True
        if (request.method not in SAFE_METHODS) and request.user.is_authenticated and not request.user.is_admin:
            fd.pop('status')
            fd.pop('manager_comments')
        return fd
    
    def to_representation(self, instance):
        a = super().to_representation(instance)
        for key, val in a.items():
            if val == None or val == '':
                a[key] = 'N/A'
        a['employee'] = instance.employee.username
        a['expense_type'] = instance.expense_type.expense_category
        return a
    
    def create(self, validated_data):
        authenticated_user = self.context.get('request').user
        validated_data['employee'] = authenticated_user
        a = super().create(validated_data)
        try:
            a.full_clean()
        except Exception as e:
            raise serializers.ValidationError(e)
        return a
    
    def update(self, instance, validated_data):
        if instance.status != 'pending' and not self.context.get('request').user.is_admin:
            raise serializers.ValidationError({'msg':'This claim cannot be updated or deleted because it has been approved or rejected'})
        return super().update(instance, validated_data)
    

class ClaimRequestSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    expense_type = serializers.SlugRelatedField(queryset=ExpenseCategory.objects.all(), slug_field='expense_category')
    class Meta:
        model = ExpenseClaim
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': True}
        }
    def get_fields(self):
        a = super().get_fields() 
        request = self.context.get('request')
        if request.method not in SAFE_METHODS and not request.user == "admin":
            fields_to_pop = ['amount','claim_description','receipt','employee','expense_type','created_at','id']
            [a.pop(x) for x in fields_to_pop]
        return a
    
    def to_representation(self, instance):
        a = super().to_representation(instance)
        if a['manager_comments'] in [None,'']:
            a['manager_comments'] = 'N/A'
        return a