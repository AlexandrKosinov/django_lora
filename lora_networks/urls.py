from django.urls import path
from . import views

urlpatterns = [
    path("owner/<int:owner_id>/", views.LoraNetworkListView.as_view()),
    path("network/<int:network_id>/", views.LoraGetawayListView.as_view()),
    path("getaway/<int:getaway_id>/", views.LoraNodeListView.as_view()),
    path("node/<int:node_id>/", views.LoraDeviceListView.as_view()),
    path("network-nodes/<int:network_id>/", views.LoraGetawayNodesListView.as_view()),
    path("user/<str:user_name>/", views.LoadUserId.as_view()),
    path("device/<int:dev_id>/", views.LoraDeviceInfoListView.as_view()),
    path("device/<int:dev_id>/<str:start_date>/<str:end_date>/", views.LoraDeviceInfoDateListView.as_view()),
    path("chart/<int:dev_id>/<str:start_date>/<str:end_date>/", views.LoraDeviceInfoChartView.as_view()),
]
