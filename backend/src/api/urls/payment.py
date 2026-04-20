from src.api.urls.base import *

urlpatterns = [
    path('payme/',              PaymeView.as_view(),             name='payme-webhook'),
    path('payme/order/',        CreatePaymeOrderView.as_view(),  name='payme-create-order'),
    path('click/',              ClickView.as_view(),             name='click-webhook'),
    path('click/order/',        CreateClickOrderView.as_view(),  name='click-create-order'),
]
