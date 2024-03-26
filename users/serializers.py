from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared.utiitys import check_email_or_phone_number, send_email, send_phone_code
from .models import User, UserConfirmation, AUTH_STATUS, AUTH_TYPE, USER_GENDER, USER_ROLES
from django.core.mail import send_mail




class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'auth_type', 'auth_status')
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }
        
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print(user)
        if user.auth_type == AUTH_TYPE.email:
            code = user.create_verify_code(AUTH_TYPE.email)
            print('code: ', code)
            send_email(user.email, code)
        elif user.auth_type == AUTH_TYPE.phone_number:
            code = user.create_verify_code(AUTH_TYPE.phone_number)
            print('code: ', code)
            send_email(user.phone_number, code)
        user.save()
        return user
        
    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data
    
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number'))
        input_type = check_email_or_phone_number(user_input)
        print("user_input: ", user_input)
        print("input_type: ", input_type)
        
        if input_type == "email":
            data = {
                "email": user_input,
                "auth_type": AUTH_TYPE.email
            }
        elif input_type == "phone_number":
            data = {
                "phone_number": user_input,
                "auth_type": AUTH_TYPE.phone_number
            }
        else:
            data = {
                "request status": "Terrible!",
                'message': "You must send email or phone number"
            }
            raise ValidationError(data)

        return data
    
    
    def validate_email_phone_number(self, value):
        if value and User.objects.filter(email=value):
            data = {
                'request status' : 'Terrible!',
                'message' : 'this email already exist!'
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone_number=value):
            data = {
                'request status' : 'Terrible!',
                'message' : 'this phone number already exist!'
            }
            raise ValidationError(data)
        return value
    
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        
        return data




class ChangeUserData(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    print('first_name: ', first_name)
    
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not first_name:
            err = {'request status' : 'bad 404', 'message' : 'you should enter first name!'}
            raise ValidationError(err)
        elif last_name:
            err = {'request status' : 'bad 404', 'message' : 'you should enter last name!'}
            raise ValidationError(err)
        elif username:
            err = {'request status' : 'bad 404', 'message' : 'you should enter username!'}
            raise ValidationError(err)
        elif password:
            err = {'request status' : 'bad 404', 'message' : 'you should enter password!'}
            raise ValidationError(err)
        elif confirm_password:
            err = {'request status' : 'bad 404', 'message' : 'you should enter  confirm password!'}
            raise ValidationError(err)
        elif password != confirm_password:
            err = {'request status' : 'bad 404', 'message' : 'your password and confirm password must be same!'}
            raise ValidationError(err)
        
    


class ChangeUserInfo(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ChangeUserData, self).__init__(*args, **kwargs)
        self.fields['confirm_password'] = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password')
        
        


