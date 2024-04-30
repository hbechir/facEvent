from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer
from .models import VerificationCode, Profile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from . import utils





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        if not profile.verified:
            return Response({'message': 'Not verified'}, status=400)
    except Profile.DoesNotExist:
        return Response({'message': 'No profile'}, status=404)
    
    return Response({'message': 'Welcome to the home page'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def finish_profile(request):
    # Add the authenticated user to the data
    data = request.data.copy()
    data['user'] = request.user.id
    # Use serializer to create the new profile
    serializer = ProfileSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        profile = serializer.save()
        if profile:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data,context={'request': request})
    if serializer.is_valid():
        user = User.objects.create_user(password=request.data.get('password'),username=request.data.get('username'))
        if user:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_code(request):
    user = request.user
    # Delete the old verification code if it was created more than 1 minute ago or if it doesn't exist
    try:
        old_verification_code = VerificationCode.objects.get(user=user)
        time_since_code_sent = timezone.now() - old_verification_code.created_at
        if time_since_code_sent > timedelta(minutes=3):
            old_verification_code.delete()
        else:
            time_left = timedelta(minutes=3) - time_since_code_sent
            return Response({'message': f'Verification code already sent, please wait for {time_left.seconds} seconds.'})
    except VerificationCode.DoesNotExist:
        pass

    # Generate and send the new verification code
    verification_code = VerificationCode.objects.create(user=user)
    print(verification_code)
    verification_code.generate_code()
    utils.send_verification_code(user.profile.phone_number, verification_code.code)
    masked_username = '*****' + user.profile.phone_number[9:]
    return Response({'message': 'Verification code sent to'+masked_username+' successfully'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request):
    user = request.user
    code = request.data.get('code')

    # Check if the code is valid
    try:
        verification_code = VerificationCode.objects.get(user=user)
    except VerificationCode.DoesNotExist:
        print('Verification code not sent')
        return Response({'message': 'Verification code not sent'}, status=400)

    if not verification_code.is_valid(user) or verification_code.code != code:
        print('Invalid verification code or expired')
        return Response({'message': 'Invalid verification code or expired'}, status=400)

    # Verify the user
    user.profile.verified = True
    user.profile.save()
    #delete the code
    verification_code.delete()

    
    return Response({'message': 'User verified successfully'})