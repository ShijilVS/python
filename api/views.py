from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .mytimer import MyTimer
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .models import Timer, ElapsedTime
t = MyTimer()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Timer API
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import Timer

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import Timer, ElapsedTime

class TimerView(APIView):
    def get(self, request):
        try:
            timer = Timer.objects.get(user=request.user)
            if timer.start_time is None:
                return Response({'status': 'Timer has not been started yet'})
            else:
                elapsed_time = timer.get_elapsed_time()
                return Response({'elapsed_time': str(elapsed_time)})
        except Timer.DoesNotExist:
            return Response({'status': 'Timer does not exist for the user'})

    def post(self, request):
        command = request.data.get('command')
        try:
            timer = Timer.objects.get(user=request.user)
        except Timer.DoesNotExist:
            timer = Timer.objects.create(user=request.user)

        if command == 'start':
            timer.start_time = datetime.now()
            timer.save()
            return Response({'status': 'Timer started'})
        elif command == 'stop':
            elapsed_time = timer.get_elapsed_time()
            
            # Save elapsed time with the current date
            elapsed_time_obj = ElapsedTime.objects.create(
                user=request.user,
                elapsed_time=elapsed_time,
                date=datetime.now().date()
            )
            
            timer.start_time = None
            timer.save()
            return Response({
                'status': 'Timer stopped',
                'elapsed_time': str(elapsed_time),
                'date': elapsed_time_obj.date
            })
        else:
            return Response({'status': 'Invalid command'})

    def get(self, request):
        timer = Timer.objects.get(user=request.user)
        if timer.start_time is None:
            return Response({'status': 'Timer has not been started yet'})
        else:
            elapsed_time = timer.get_elapsed_time()
            return Response({'elapsed_time': str(elapsed_time)})
    


    def post(self, request):
        command = request.data.get('command')
        if command == 'start':
            t.start()
            return Response({'status': 'Timer started'})
        elif command == 'stop':
            elapsed_time = t.get()
            t.stop()
            return Response({'status': 'Timer stopped', 'elapsed_time': str(elapsed_time)})
        else:
            return Response({'status': 'Invalid command'})

class ElapsedTimeView(APIView):
    def get(self, request):
        user = request.user
        timer = Timer.objects.filter(user=user, end_time__isnull=False).latest('end_time')
        elapsed_time = timer.elapsed_time if timer.elapsed_time else timer.end_time - timer.start_time
        return Response({'elapsed_time': str(elapsed_time)})