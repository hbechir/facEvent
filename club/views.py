from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render
from .serializers import ClubSerializer,MembershipSerializer
from .models import Club,Membership
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_club(request):
    if request.user.profile.is_admin == False:
        return Response({'error': 'You are not authorized to add a club'}, status=status.HTTP_403_FORBIDDEN)
    else:    
        serializer = ClubSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            club = serializer.save()
            if club:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_club(request):
    if request.user.profile.is_admin == False:
        return Response({'error': 'You are not authorized to delete a club'}, status=status.HTTP_403_FORBIDDEN)
    else:    
        club = Club.objects.get(id=request.data['id'])
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_club(request):
    if request.user.profile.is_admin == False:
        return Response({'error': 'You are not authorized to update a club'}, status=status.HTTP_403_FORBIDDEN)
    else:
        club = Club.objects.get(id=request.data['id'])
        # Update only the provided fields in the request
        serializer = ClubSerializer(instance=club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_clubs(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_membership(request):
    club = Club.objects.get(id=request.data['id'])
    # check if the manager is the same as the user
    if club.manager == request.user:
        return Response({'error': 'You are the manager of the club'}, status=status.HTTP_403_FORBIDDEN)
    
    # check if the user has no previous pending or active requests
    existing_membership = Membership.objects.filter(user=request.user, club=club, state__in=['PENDING', 'ACTIVE'])
    if existing_membership.exists():
        return Response({'error': 'You already have a pending or active membership request'}, status=status.HTTP_400_BAD_REQUEST)

    serializer_input = {'club': club.id, 'user': request.user.id,'note': request.data['note']}
    serializer = MembershipSerializer(data=serializer_input, context={'request': request})
    if serializer.is_valid():
        membership = serializer.save()
        if membership:
            return Response({"message": "Membership request sent successfully, waiting for approval from the club manager"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_club_membership_state(request):
    # get the club from the providid membership id
    membership = Membership.objects.get(id=request.data['membership_id'])
    club = membership.club
    
    # check if user is the same as the club manager
    if club.manager != request.user:
        return Response({'error': 'You are not authorized to change the membership state'}, status=status.HTTP_403_FORBIDDEN)
    
    membership_state=membership.toggle_club_membership_state()


    return Response({"state":membership_state}, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_club_memberships(request):

    # get the club of which the id is passed in the request
    club = Club.objects.get(id=request.data['club_id'])

    # check if the user is the manager of the club
    if club.manager != request.user:
        return Response({'error': 'You are not authorized to view the memberships'}, status=status.HTTP_403_FORBIDDEN)
    
    memberships = Membership.objects.filter(club=club)
    serializer = MembershipSerializer(memberships, many=True)
    
    return Response(serializer.data)