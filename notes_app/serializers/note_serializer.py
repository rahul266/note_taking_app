from rest_framework import serializers
from ..models import Note,NoteVersion

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner','last_edited_by', 'created_at', 'updated_at']
        extra_kwargs = {'owner': {'read_only': True},'last_edited_by':{'read_only': True}}

class NoteVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteVersion
        fields = ['id', 'note', 'title', 'content', 'created_at', 'editor']