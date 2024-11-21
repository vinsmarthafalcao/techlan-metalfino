from django.db.models import Model

class SeniorModel(Model):
    class Meta:
        abstract = True
        
    def related(self, model:Model):
        try: 
            keys = model._meta.unique_together[0]
            filter_kwargs = {field: getattr(self, field) for field in keys if hasattr(self, field)}
            return model.objects.get(**filter_kwargs)
        except: return None

    
        