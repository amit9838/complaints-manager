from import_export import resources
from complaint.models import Complaint , Item, CheckList

class ComplaintResource(resources.ModelResource):
    class Meta:
        model = Complaint