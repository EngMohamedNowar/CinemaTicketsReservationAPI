from django.shortcuts import render
from .models import Guest
from rest_framework.decorators import api_view
from .serializers import GuestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework  import status ,filters
from django.http import Http404
from rest_framework import generics ,mixins
# Create your views here.
# FUNCTION BASED VIEWS
# @api_view('GET','PUT','DELETE')
# def FBV_pk(request,pk):
#     try:
#         guests = Guest.objects.get(pk=pk)
#     except Guest.DoesNotExist:
#             return Response(status = 404)
#     if request.method == 'GET':
#         serializer = GuestSerializer(guests)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = GuestSerializer(guests,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = 201)
#         return Response(serializer.errors, status = 400)
#     if request.method == 'DELETE':
#         guests = Guest.delete()
#         return Response(status = 204)

# CLASS BASED VIEWS
# list and create  == GET ,POST
class CBV_list(APIView):
    # GET request to list all guests
    def get(self, request):
        guests = Guest.objects.all()  # Retrieve all guests
        serializer = GuestSerializer(guests, many=True)  # Serialize the list of guests
        return Response(serializer.data)  # Return the serialized data as a response
    # POST request to add a new guest
    def post(self, request):
        serializer = GuestSerializer(data=request.data)  # Create a serializer with the request data
        if serializer.is_valid():  # Check if the data is valid
            serializer.save()  # Save the new guest object
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respond with the created guest data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
class CBV_PK(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk) 
        except Guest.DoesNotExist:
            raise Http404
    # GET request to retrieve a specific guest
    def get(self,request,pk):
        guests = self.get_object(pk)
        serializer = GuestSerializer(guests)
        return Response(serializer.data)
    # PUT request to update a specific guest
    def put(self, request, pk):
        guests = self.get_object(pk)
        serializer = GuestSerializer(guests, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE request to delete a specific guest
    def delete(self, request, pk):
        guests = self.get_object(pk)
        guests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# mixins list GET ,POST
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
 # mixins pk GET PUT DELETE
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request,pk):
        return self.retrieve(request, pk)
    def put(self, request, pk):
        return self.update(request, pk)
    def delete(self,request,pk):
        return self.destroy(request,pk)
    

#Generics GET , POST
class Generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','mobile']

#Generics GET , PUT , DELETE
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','mobile']

