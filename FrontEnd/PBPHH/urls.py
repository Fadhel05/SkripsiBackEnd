from django.urls import path, include
from rest_framework.routers import DefaultRouter

from FrontEnd.PBPHH.views import PegawaiView, PermohonanView, DokumenView, testCreateDokumen

router = DefaultRouter()

router.register(r'create/pegawai',PegawaiView)
router.register(r'test',testCreateDokumen)
urlpatterns = [

    path('', include(router.urls)),
    path('login',PegawaiView.as_view({"post":"login"})),
    path('get/permohonan/skala/besar/<str:ranger>/',PermohonanView.as_view({"get":"listsheet"})),
    path('get/permohonan/skala/kecil/<str:ranger>/',PermohonanView.as_view({"get":"listshee"})),
    path('edit/permohonan/skala/kecils/<int:pk>/',PermohonanView.as_view({"put":"updateskala"})),
    path('edit/dokumen/',testCreateDokumen.as_view({"post":"editdokumen"})),
    path('see/dokumen/<str:namadok>/',testCreateDokumen.as_view({"get":"seedokumen"})),
    path('edit/permohonan/skala/kecil/<int:pk>/',PermohonanView.as_view({"put":"listkele"})),
    path('edit/permohonan/skala/besar/<int:pk>/',PermohonanView.as_view({"put":"listkeles"})),
    path('create/permohonan/skala/besar',PermohonanView.as_view({"post":"createskalabesar"})),
    path('list/permohonan/skala/besar',PermohonanView.as_view({"get":"listskalabesar"})),
    path('list/permohonan/skala/kecil',PermohonanView.as_view({"get":"listskalakecil"})),
    path('lihat/note/dokumen/<int:pk>', DokumenView.as_view({"put": "lihatnotedokumen"})),
    path('note/dokumen/<int:pk>', DokumenView.as_view({"put": "notedokumen"})),

]