from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Comment, Review


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
        request = self.context.get['request']
        if request.method == 'POST':
            title = data['title']
            if title.reviews.filter(author=request.user).exists():
                raise serializers.ValidationError(
                    'На это произведение вы уже оставляли отзыв.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only =True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
