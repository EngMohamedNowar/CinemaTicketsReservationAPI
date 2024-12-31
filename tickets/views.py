from django.shortcuts import render
from .models import Guest , Movie , Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer ,MovieSerializer ,ReservationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework  import status ,filters
from django.http import Http404
from rest_framework import generics ,mixins ,viewsets
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


# Viewsets Guests
class Viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','mobile']

 # Viewsets Movie
class Viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie','hall']
# Viewsets reservations
class Viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['guest','movie']


# Function To Find Movie
@api_view(['GET'])
def find_movie(request):
    # Retrieve query parameters
    movie_name = request.query_params.get('movie')  # Correct field name
    
    # Validate query parameters
    if not movie_name:
        return Response(
            {"error": "'movie' query parameters are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Filter movies
    movies = Movie.objects.filter(movie=movie_name)  # Adjust fields if necessary
    
    if not movies.exists():
        return Response(
            {"message": "No movies found matching the given criteria."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serialize and return data
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_reservation(request):
    try:
        # Retrieve the movie based on the provided `hall` and `movie` values
        movie = Movie.objects.get(
            hall=request.query_params.get('hall'),
            movie=request.query_params.get('movie')
        )
    except Movie.DoesNotExist:
        return Response(
            {"error": "Movie not found with the provided hall and movie name."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Create a new guest
    guest = Guest.objects.create(
        name=request.query_params.get('name'),
        mobile=request.query_params.get('mobile')
    )

    # Create a new reservation
    reservation = Reservation.objects.create(
        guest=guest,
        movie=movie
    )
    
    #serializer
    serializer = ReservationSerializer(reservation)
    # return Response(serializer.data)
    

    # Return success response with guest name
    return Response(
        serializer.data, status=status.HTTP_201_CREATED 
    )
