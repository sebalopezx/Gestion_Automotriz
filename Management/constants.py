from .models import ConfigConstant

POINTS = ConfigConstant.objects.get(name='POINTS').value