from django.db.models import Field
from ..utils import HalfVector


# https://docs.djangoproject.com/en/5.0/howto/custom-model-fields/
class HalfVectorField(Field):
    description = 'Half vector'
    empty_strings_allowed = False

    def __init__(self, *args, dimensions=None, **kwargs):
        self.dimensions = dimensions
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.dimensions is not None:
            kwargs['dimensions'] = self.dimensions
        return name, path, args, kwargs

    def db_type(self, connection):
        if self.dimensions is None:
            return 'halfvec'
        return 'halfvec(%d)' % self.dimensions

    def from_db_value(self, value, expression, connection):
        return HalfVector.from_db(value)

    def to_python(self, value):
        return HalfVector.from_db(value)

    def get_prep_value(self, value):
        return HalfVector.to_db(value)

    def value_to_string(self, obj):
        return self.get_prep_value(self.value_from_object(obj))
