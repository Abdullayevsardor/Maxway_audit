from rest_framework import serializers
from .models import Category, Item, Branch, Score

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "text",)

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ("id", "name", "items")

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("id", "name")

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ("id", "branch", "item", "score", "image", "created_at")
