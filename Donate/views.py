from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from Donate.models import Donate
from Donate.serializers import DonateCreateSerializer
from Post.models import Post

# Create your views here.
# Create your views here.
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_donate_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['account_id'] = request.user.pk
        serializer = DonateCreateSerializer(data = data)
        
        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            donate = serializer.save()
            data['donate_id'] = donate.pk
            data['account_id_from'] = donate.account_id_from.pk
            data['post_id_to'] = donate.post_id_to.pk
            data['amount'] = donate.amount
            data['is_recurring'] = donate.is_recurring
            if (donate.occurence is not None):
                data['occurence'] = donate.occurence
            else:
                data['occurence'] = None
            data['start_date'] = donate.start_date
            data['times_donated'] = donate.times_donated
            data['username'] = donate.account_id_from.username

            post = Post.objects.get(pk = data['post_id_to'])
            prev_current_dollar = post.current_dollar
            Post.objects.filter(pk=data['post_id_to']).update(current_dollar = prev_current_dollar + data['amount'])
            print(prev_current_dollar)

            print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)