from rest_framework import viewsets, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from districts.serializers import *


# Regions ViewSet Class
class Regions_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all Regions handled here
        queryset = Regions.objects.all()
        serializer = Regions_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = Regions_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific Region handled here
        try:
            queryset = get_object_or_404(Regions, pk=pk)
        except Regions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Regions_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    def update(self, request, pk=None): # PUT method handled here - Updating record
        try:
            queryset = Regions.objects.get(pk=pk)
        except Regions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Regions_Serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None): # DELETE method handled here
        try:
            queryset = Regions.objects.get(pk=pk)
        except Regions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Districts ViewSet Class
class Districts_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all Districts handled here
        queryset = Districts.objects.all()
        serializer = Districts_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = Districts_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific District handled here
        try:
            queryset = get_object_or_404(Districts, pk=pk)
        except Districts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Districts_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


# County ViewSet Class
class County_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all County handled here
        queryset = County.objects.all()
        serializer = County_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = County_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific County handled here
        try:
            queryset = get_object_or_404(County, pk=pk)
        except County.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = County_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


# SubCounty ViewSet Class
class SubCounty_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all SubCounty handled here
        queryset = SubCounty.objects.all()
        serializer = SubCounty_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = SubCounty_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific SubCounty handled here
        try:
            queryset = get_object_or_404(SubCounty, pk=pk)
        except SubCounty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubCounty_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


# Parish ViewSet Class
class Parish_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all Parish handled here
        queryset = Parish.objects.all()
        serializer = Parish_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = Parish_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific Parish handled here
        try:
            queryset = get_object_or_404(Parish, pk=pk)
        except Parish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Parish_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


# Location ViewSet Class
class Location_ViewSet(viewsets.ViewSet):
    
    def list(self, request): # GET method for list of all Location handled here
        queryset = Location.objects.all()
        serializer = Location_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # POST method handled here
        serializer = Location_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): # GET method for a specific District handled here
        try:
            queryset = get_object_or_404(Location, pk=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Location_Serializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
