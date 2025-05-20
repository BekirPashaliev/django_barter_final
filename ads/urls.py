from django.urls import path
from . import views
app_name = 'ads'
urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_edit'),
    path('ads/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('proposals/', views.ExchangeProposalListView.as_view(), name='proposal_list'),
    path('proposals/create/', views.ExchangeProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/<int:pk>/update/', views.ExchangeProposalUpdateView.as_view(), name='proposal_update'),
]

