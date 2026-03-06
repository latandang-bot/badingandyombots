from .models import LearningUnit

def nav_units(request):
    # only LU3-LU7
    units = LearningUnit.objects.filter(name__in=["LU3", "LU4", "LU5", "LU6", "LU7"]).order_by("name")
    return {"nav_units": units}