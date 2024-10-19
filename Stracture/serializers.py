from rest_framework import serializers
from . import models  
from rest_framework import serializers





class SelectTimeSerializer(serializers.ModelSerializer):
    # consultant = serializers.PrimaryKeyRelatedField(queryset=models.Consultant.objects.all())

    class Meta:
        model = models.SelectTime
        fields = '__all__'   

