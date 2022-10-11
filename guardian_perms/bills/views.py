# from viewflow.flow.views import (
#    DetailProcessView as BaseDetailProcessView,
#    CancelProcessView as BaseCancelProcessView
# )
# from viewflow.workflow.flow.views import ProcessListView as BaseProcessListView
# from viewflow.frontend.viewset import FlowViewSet


# class ProcessListView(BaseProcessListView):
#     def get_queryset(self):
#         return super(ProcessListView, self).get_queryset()


# class DetailProcessView(BaseDetailProcessView):
#     def get_queryset(self):
#         return super(DetailProcessView, self).get_queryset()


# class CancelProcessView(BaseCancelProcessView):
#     def get_queryset(self):
#         return super(CancelProcessView, self).get_queryset()


# class BillFlowViewSet(FlowViewSet):
#     def get_process_queryset(self, request):
#         pass

#     process_list_view = [
#         r'^$',
#         ProcessListView.as_view(),
#         'index'
#     ]

#     detail_process_view = [
#         r'^(?P<process_pk>\d+)/$',
#         DetailProcessView.as_view(),
#         'detail'
#     ]

#     cancel_process_view = [
#         r'^action/cancel/(?P<process_pk>\d+)/$',
#         CancelProcessView.as_view(),
#         'action_cancel'
#     ]
