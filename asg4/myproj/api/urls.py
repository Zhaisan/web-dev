from django.urls import path, include

urlpatterns = [
    path('v1/', include(('api.urls_v1', 'api_v1'), namespace='v1')),
    path('v2/', include(('api.urls_v2', 'api_v2'), namespace='v2')),
]