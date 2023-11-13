from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from .serializer import CarShowRoomSerializerList,CarShowRoomSerializerCreate
from .models import CarShowRoom 

class CarShowRoomListCreateAPIView(ListCreateAPIView, GenericViewSet):
    queryset = CarShowRoom.objects.all()
    serializer_class = CarShowRoomSerializerList

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarShowRoomSerializerCreate
        return super().get_serializer_class()

# class CarShowRoomDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # queryset = CarShowRoom.objects.all()
    # serializer_class = CarShowRoomSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)