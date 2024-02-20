from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import *
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from ..serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.exceptions import PermissionDenied


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    try:
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user,last_edited_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as excetion:
        print(excetion)
        return Response({'message':'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def get_note_detail(request, id):
    try:
        try:
            note = Note.objects.get(id=id)
            if note.owner == request.user or NoteEditPermissionsTable.objects.filter(user=request.user, note=note).exists():
                serializer = NoteSerializer(note)
                return Response(serializer.data)
            else:
                raise PermissionDenied("You do not have permission to access this note.")
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message':'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    try:
        note_id = request.data.get('note_id')
        user_emails = request.data.get('user_emails', [])

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response("Note not found", status=status.HTTP_404_NOT_FOUND)

        if note.owner != request.user:
            return Response("You do not have permission to share this note", status=status.HTTP_403_FORBIDDEN)

        users_to_share_with = []
        for email in user_emails:
            try:
                user = User.objects.get(email=email)
                if not NoteEditPermissionsTable.objects.filter(user=user, note=note).exists():
                    users_to_share_with.append(user)
            except ObjectDoesNotExist:
                pass

        for user in users_to_share_with:
            NoteEditPermissionsTable.objects.create(user=user, note=note)

        return Response("Note shared successfully", status=status.HTTP_200_OK)
    except:
        return Response({'message':'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def update_note(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response("Note not found", status=status.HTTP_404_NOT_FOUND)

    if note.owner != request.user and not NoteEditPermissionsTable.objects.filter(user=request.user, note=note).exists():
        return Response("You do not have permission to edit this note", status=status.HTTP_403_FORBIDDEN)


    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
        NoteVersion.objects.create(
            note=note,
            title=note.title,
            content=note.content,
            created_at=note.updated_at,
            editor=note.last_edited_by
        )
        serializer.save(owner=note.owner,last_edited_by=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def get_or_update_note(request,id):
    if(request.method == 'GET'):
        return get_note_detail(request,id)
    elif(request.method=='PUT'):
        return update_note(request,id)
    return Response({'message':'please check method'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        try:
            note = Note.objects.get(id=id)
        except Note.DoesNotExist:
            return Response("Note not found", status=status.HTTP_404_NOT_FOUND)

        if note.owner != request.user and not NoteEditPermissionsTable.objects.filter(user=request.user, note=note).exists():
            return Response("You do not have permission to access this note", status=status.HTTP_403_FORBIDDEN)
        
        current_version=NoteSerializer(note)
        
        versions = NoteVersion.objects.filter(note=note).order_by('-created_at')
        version_history_serializer = NoteVersionSerializer(versions, many=True)

        response_data = {
            'currentVersion': current_version.data,
            'versionHistory': version_history_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except:
        return Response({'message':'somthing went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
