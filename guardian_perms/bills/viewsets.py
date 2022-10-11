from viewflow.urls import ReadonlyModelViewset, ModelViewset
from . import models


class BillViewset(ReadonlyModelViewset):
    model = models.Bill
    icon = 'receipt'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DepartmentViewset(ModelViewset):
    model = models.Department
    icon = 'corporate_fare'
