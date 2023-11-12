from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import GenericAPIView
from .serializer import CarShowRoomSerializer
from .models import CarShowRoom 

class CarShowRoomListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = CarShowRoom.objects.all()
    serializer_class = CarShowRoomSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class CarShowRoomDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # queryset = CarShowRoom.objects.all()
    # serializer_class = CarShowRoomSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)