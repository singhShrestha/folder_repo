from import_export import resources
from .models import *

class QuestionResource(resources.ModelResource):
    class Meta:
        model=QuestionTable