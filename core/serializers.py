# core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Member, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
# just added email
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # ✅ Add this create method here
    def create(self, validated_data):
        # Check if username already exists
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"error": "Username already exists"})
        # Check if email already exists
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"error": "Email already registered"})
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Also create a related Member record
        Member.objects.create(user=user)
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    borrower_username = serializers.CharField(source="member.user.username", read_only=True)
    borrower_email = serializers.CharField(source="member.user.email", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "book",
            "member",
            "borrow_date",
            "due_date",
            "return_date",
            "fine",
            "borrower_username",
            "borrower_email",
            "book_title",
        ]

        
# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'



class TransactionDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)
    borrower_email = serializers.EmailField(source="member.user.email", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "book_title",
            "book_author",
            "borrower_email",
            "borrow_date",
            "due_date",
            "return_date",
            "fine",
            "extended",
        ]
##just added this
