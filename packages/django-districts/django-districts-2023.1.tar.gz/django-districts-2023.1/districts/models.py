from django.db import models

# Regions Model.
class Regions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.region
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Region"


# Districts/City Model.
class Districts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    district = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.district
    
    class Meta:
        verbose_name = "District/City"
        verbose_name_plural = "District/City"


# County/Municipality Model.
class County(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    county = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.county
    
    class Meta:
        verbose_name = "County/Municipality"
        verbose_name_plural = "County/Municipality"


# SubCounty Model.
class SubCounty(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    sub_county = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_county
    
    class Meta:
        verbose_name = "Sub-County/Town Council/Division"
        verbose_name_plural = "Sub-County/Town Council/Division"


# Parish Model.
class Parish(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)
    parish = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parish
    
    class Meta:
        verbose_name = "Parish/Ward"
        verbose_name_plural = "Parish/Ward"


# Location Model.
class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    parish = models.OneToOneField(Parish, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lat: { self.latitude }, Long: { self.longitude }"
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Location"
