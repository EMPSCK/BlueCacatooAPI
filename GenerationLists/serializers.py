
from rest_framework import serializers
from .models import CompetitionJudges


class JudgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionJudges
        fields = ('id', 'lastname', 'firstname', 'sport_category', 'regionid', 'club', 'booknumber')
