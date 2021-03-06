from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from event.models import Event
from event.serializers import EventCreateSerializer, EventUpdateSerializer, EventSerializer
from participant.models import Participant

# Create your views here.
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_event_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['creator'] = request.user.pk
        serializer = EventCreateSerializer(data = data)
        
        fields = ['creator', 'title', 'location', 'date', 'description', 'duration', 'event_pic', 'participant_count']

        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            event = serializer.save()
            data['event_id'] = event.pk
            data['creator'] = event.creator.pk
            data['title'] = event.title
            data['location'] = event.location
            data['date'] = event.date
            data['description'] = event.description
            data['duration'] = event.duration
            data['creator_username'] = event.creator.username
            data['event_pic'] = event.event_pic
            data['participant_count'] = event.participant_count

            print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def change_event_view(request):
    try:
        event = Event.objects.get(pk = request.data['event_id'])
        print(event)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if event.creator != user:
        return Response({'response':"You don't have permission to edit that."}) 
        
    if request.method == 'PUT':
        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'UPDATE SUCCESS'
            data['title'] = event.title
            data['location'] = event.location
            data['date'] = event.date
            data['description'] = event.description
            data['duration'] = event.duration
            data['event_pic'] = event.event_pic
            data['participant_count'] = event.participant_count
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([])
class EventListView(ListAPIView):
    serializer_class = EventSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Event.objects.all().order_by('-date')
        return queryset

@permission_classes([])
class ProfileEventsView(ListAPIView):
    serializer_class = EventSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = Event.objects.filter(creator=user_id).order_by('-date')
            print(queryset)
        else: 
            queryset = Event.objects.all().order_by('-date')

        return queryset

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_user_attending_events_view(request):
    user = request.user.pk
    #eventset = user.event.all()
    eventset = Participant.objects.filter(user_id=user)
    print(eventset)
    ret = [EventSerializer(y.event).data for y in eventset]
    return Response({'events': ret})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_event_view(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.get(pk=event_id)
    except:
        return Response({'response': 'Event does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def is_attending_event(request):
    #event_id = request.GET.get('event_id')
    data = {
        'user_id': request.user.pk,
        'event': request.GET.get('event_id'),
    }
    print(data['event'])
    try:
        is_attending = Participant.objects.filter(user_id=data['user_id']).filter(event=data['event'])
    except:
        return Response({'response': 'Participant at this Event does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    #serializer = EventSerializer(is_attending)
    if (is_attending.exists()):
        ret = {
            'attending' : True
        }
    else:
        ret = {
            'attending' : False
        }
    #print(is_attending)
    return Response(ret)
