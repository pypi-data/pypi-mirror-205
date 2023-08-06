from django.contrib import admin

from districts.models import County, Regions, Districts, SubCounty, Parish, Location

# Regions Admin Model.
class Regions_Admin(admin.ModelAdmin):
    fields = [
        "region",
    ]

    list_display = (
        "id", "region", "created_at", "updated_at"
    )

admin.site.register(Regions, Regions_Admin)


# Districts Admin Model.
class Districts_Admin(admin.ModelAdmin):
    fields = [
        "region", "district",
    ]

    list_display = (
        "id", "region", "district", "created_at", "updated_at"
    )

admin.site.register(Districts, Districts_Admin)


# County Admin Model.
class County_Admin(admin.ModelAdmin):
    fields = [
        "district", "county",
    ]

    list_display = (
        "id", "district", "county", "created_at", "updated_at"
    )

admin.site.register(County, County_Admin)


# SubCounty Admin Model.
class SubCounty_Admin(admin.ModelAdmin):
    fields = [
        "county", "sub_county",
    ]

    list_display = (
        "id", "county", "sub_county", "created_at", "updated_at"
    )

admin.site.register(SubCounty, SubCounty_Admin)


# Parish Admin Model.
class Parish_Admin(admin.ModelAdmin):
    fields = [
        "sub_county", "parish",
    ]

    list_display = (
        "id", "sub_county", "parish", "created_at", "updated_at"
    )

admin.site.register(Parish, Parish_Admin)


# Location Admin Model.
class Location_Admin(admin.ModelAdmin):
    fields = [
        "parish", "latitude", "longitude",
    ]

    list_display = (
        "id", "parish", "latitude", "longitude", "created_at", "updated_at"
    )

admin.site.register(Location, Location_Admin)
