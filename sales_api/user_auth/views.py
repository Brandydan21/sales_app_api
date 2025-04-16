# views.py
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.contrib.auth import authenticate


# gets the user model that is defined in the auth_user_model in settings.py
User = get_user_model()


class UserViewSet(ModelViewSet):
    '''
    The ModelViewSet class defines the CRUD methods
    (list, retrieve, create, update, delete)
    '''

    # this is getting all the User records on the User table it will be a list
    # of User django model objects
    queryset = User.objects.all()

    serializer_class = UserSerializer

    # overload the create method
    def create(self, request, *args, **kwargs):
        
        # gets an instance of our serializer class
        serializer = self.get_serializer(data=request.data)

        # checks if serializer is valid
        serializer.is_valid(raise_exception=True)
        
        # calls the .create() serializer method as we are creating a new object
        user = serializer.save()

        # Generate JWT token for the user created
        # returning the refresh and access token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': access_token,
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        
        #GET /users/5/ this is getting user with id 5 for example
        user_to_update = self.get_object()
        
        
        if request.user != user_to_update:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # gets a serializer and create 
        serializer = self.get_serializer(user_to_update, data=request.data, partial=True) 
        # validates the data and returns an exception if failed
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )