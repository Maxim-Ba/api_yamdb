from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        

    class Meta:
        model = Review
        fields = ('__all__',)
