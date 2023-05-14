from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
	username = request.data['username']
	if username:
		user = get_object_or_404(User, username=username)
		managers = Group.objects.get(name="Manager")
		if request.method == 'POST':
			managers.user_set.add(user)
		if request.method == 'DELETE':
			managers.user_set.remove(user)
		return Response({'message':f'user {username} successfully added'})
	
	return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class MenuItemViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer	
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

