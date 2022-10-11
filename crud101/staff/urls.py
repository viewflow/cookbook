from viewflow import Icon
from viewflow.urls import Application
from . import viewset


class StaffApp(Application):
    title = 'Staff Management'
    icon = Icon('groups')
    permission=lambda user: user.is_staff,
    viewsets = [
        viewset.DepartmentViewset(),
        viewset.EmployeeViewset()
    ]
