from rest_framework import serializers

from core.models import Tag, Ingrediant, Recipe


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngrediantSerializer(serializers.ModelSerializer):
    """Serializer for ingrediant objects"""

    class Meta:
        model = Ingrediant
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer fom a recipe"""
    ingrediants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingrediant.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingrediants', 'tags', 'time_minutes',
                  'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingrediants = IngrediantSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
