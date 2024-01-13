from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from FrontEnd.PBPHH.Serializers import PegawaiSerializer, PermohonanSerializer, PerusahaanSerializer, DokumenSerializer
from FrontEnd.PBPHH.models import PegawaiModel, PermohonanModel, DokumenModel, PerusahaanModel
import os
import json




class PegawaiView(viewsets.ModelViewSet):
    queryset = PegawaiModel.objects.all()
    serializer_class = PegawaiSerializer

    def create(self, request, *args, **kwargs):
        # try:
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        print(serializers.data['id_pegawai'])
        # except:
        #     fail=True
        #     # print("why",serializer.data)
        #     pass
        # if fail:
        #     return Response({'data':'failed'},status.HTTP_400_BAD_REQUEST)
        return Response(serializers.data,status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(),many=True)
        return Response(serializer.data,status.HTTP_200_OK)

class PermohonanView(viewsets.ModelViewSet):
    queryset = PermohonanModel.objects.all()
    query_perusahaan = PerusahaanModel.objects.all()
    query_dokumen = DokumenModel.objects.all()
    serializer_class = PermohonanSerializer
    @action(detail=False,methods=["get"])
    def listsheet(self,request,*args,**kwargs):
        query = self.queryset.filter(posisi=kwargs["ranger"],skala="Besar")
        serial = self.serializer_class(query,many=True)
        mentah = serial.data[::-1]
        jeng=[]
        jing=[]
        for x in range(len(mentah)):
            if((x+1)%2==0):
                jing.append(mentah[x])
                jeng.append(jing)
                jing = []
            else:
                jing.append(mentah[x])
        if len(jing)>0:
            jeng.append(jing)
        return Response(jeng,status=status.HTTP_200_OK)
    @action(detail=False,methods=["get"])
    def listshee(self,request,*args,**kwargs):
        print(kwargs)
        query = self.queryset.filter(posisi=kwargs["ranger"],skala="Kecil")
        serial = self.serializer_class(query,many=True)
        return Response(serial.data,status=status.HTTP_200_OK)
    @action(detail=False, method=['put'])
    def listkele(self,request,*args,**kwargs):
        try:
            print("serial", self.queryset.get(id_request=kwargs["pk"], skala="Kecil"))
            serial = self.serializer_class(self.queryset.get(id_request=kwargs["pk"], skala="Kecil"))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # serializer = self.serializer_class(self.get_queryset().filter(skala="Besar"),many=True)
        return Response(serial.data,status.HTTP_200_OK)
    @action(detail=False, method=['put'])
    def listkeles(self,request,*args,**kwargs):
        serial = self.serializer_class(self.queryset.get(id_request=kwargs["pk"],skala="Besar"))
        # print(serial.data)
        # serializer = self.serializer_class(self.get_queryset().filter(skala="Besar"),many=True)
        return Response(serial.data,status.HTTP_200_OK)
    @action(detail=False, method=['get'])
    def listskalabesar(self,request,*args,**kwargs):
        serializer = self.serializer_class(self.get_queryset().filter(skala="Besar"),many=True)
        return Response(serializer.data,status.HTTP_200_OK)

    @action(detail=False, method=['get'])
    def listskalakecil(self,request,*args,**kwargs):
        serializer = self.serializer_class(self.get_queryset().filter(skala__icontains="Kecil"),many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    @action(detail=False, method=['post'])
    def createskalabesar(self,request,*args,**kwargs):
        request.data["Perusahaan"]["jenis_produk"] = json.dumps(request.data["Perusahaan"]["jenis_produk"])
        request.data["Perusahaan"]["daftar_mesin"] = json.dumps(request.data["Perusahaan"]["daftar_mesin"])
        print(request.data)
        serialperusahaan = PerusahaanSerializer(data=request.data["Perusahaan"])
        serialperusahaan.is_valid(raise_exception=True)
        serialperusahaan.save()
        request.data["Permohonan"]["id_perusahaan"] = serialperusahaan.data["id_perusahaan"]

        serializers = self.serializer_class(data=request.data["Permohonan"])
        serializers.is_valid(raise_exception=True)
        serializers.save()

        print("pass")
        # for e in request.data["Dokumen"]:
        #     print(e)
        #     e["id_permohonan"] = serializers.data["id_request"]
            # filee = e.pop("dataDokumen")
            # hehe = open(filee, "wb")
            # print(filee,type)
        doh = [];
        for e in request.data["Dokumen"]:
            dih = request.data["Dokumen"][e]
            dih["id_permohonan"] = serializers.data["id_request"]
            doh.append(dih);
            # filee = e.pop("dataDokumen")
            # hehe = open(filee, "wb")
            # print(filee,type)
        serializerss = DokumenSerializer(data=doh,many=True)
        serializerss.is_valid(raise_exception=True)
        serializerss.save()
        data = {**serializers.data}
        data["dokumen"] = serializerss.data
        return Response({"data":data},status.HTTP_200_OK)
    @action(detail=False, methods=["put"])
    def updateskala(self, request, *args, **kwargs):
        request.data["Perusahaan"]["jenis_produk"] = json.dumps(request.data["Perusahaan"]["jenis_produk"])
        request.data["Perusahaan"]["daftar_mesin"] = json.dumps(request.data["Perusahaan"]["daftar_mesin"])
        # print(request.data);
        id_perusahaan = request.data["Perusahaan"]["id_perusahaan"]
        serialperusahaan = PerusahaanSerializer(instance=self.query_perusahaan.get(id_perusahaan=id_perusahaan),data=request.data["Perusahaan"],partial=True)
        serialperusahaan.is_valid(raise_exception=True)
        serialperusahaan.save()

        serializers = self.serializer_class(instance=self.get_object(),data=request.data["Permohonan"],partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        # for e in request.data["Dokumen"]:
        #     print(e)
        #     e["id_permohonan"] = serializers.data["id_request"]
            # filee = e.pop("dataDokumen")
            # hehe = open(filee, "wb")
            # print(filee,type)
        doh = [];
        for e in request.data["Dokumen"]:
            dih = request.data["Dokumen"][e]["id_dokumen"]
            serializerss = DokumenSerializer(instance=self.query_dokumen.get(id_dokumen=dih),data=request.data["Dokumen"][e],partial=True)
            serializerss.is_valid(raise_exception=True)
            serializerss.save()
            doh.append(serializerss.data);

        print("pass")
        data = {**serializers.data}
        data["dokumen"] = serializerss.data
        return Response({"data":data},status.HTTP_200_OK)
class DokumenView(viewsets.ModelViewSet):
    queryset = DokumenModel.objects.all()
    serializer_class = DokumenSerializer

    @action(detail=False, methods=['put'])
    def notedokumen(self,request,*args,**kwargs):
        dataBang = self.get_queryset().filter(id_permohonan=kwargs['pk'])
        data = []
        for e in range( len(dataBang)):
            serializers = self.get_serializer(dataBang[e],data=request.data[e])
            serializers.is_valid(raise_exception=True)
            serializers.save()
            data.append(serializers.data)
        return Response(data,status.HTTP_200_OK)
    @action(detail=False, methods=['put'])
    def lihatnotedokumen(self,request,*args,**kwargs):
        print(kwargs)
        dataBang = self.get_serializer(self.get_queryset().filter(id_permohonan=kwargs['pk']),many=True)

        # print(dataBang)
        return Response(dataBang.data,status.HTTP_200_OK)
class testCreateDokumen(viewsets.ModelViewSet):
    queryset = DokumenModel.objects.all()
    serializer_class = DokumenSerializer
    def create(self, request, *args, **kwargs):
        print("test",type(request.data["dataDokumen"]))
        FileSystemStorage(location="").save("dokumen/"+request.data["namaDokumen"], request.data["dataDokumen"])
        # file = open("fdsaffsda.pdf","wb")
        # file.writeable(request.data["dataDokumen"])
        # file.close()
        return Response({"data":"data"},status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def editdokumen(self, request, *args, **kwargs):
        print(kwargs,request.data["namaDokumen"])
        try:
            os.remove("dokumen/%s"%request.data["namaDokumen"])
        except Exception as e:
            print(e)
        FileSystemStorage(location="").save("dokumen/" + request.data["namaDokumen"], request.data["dataDokumen"])
        return Response({"data":"data"},status.HTTP_200_OK)
        # return response
    @action(detail=False, methods=['get'])
    def seedokumen(self, request, *args, **kwargs):
        filex = open("dokumen/%s.pdf"%kwargs["namadok"],"rb")
        response = HttpResponse(filex.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=surat_permohonan.pdf'
        response['X-Frame-Options'] = 'ALLOW FROM * http://localhost:3000/ http://localhost:3000'
        # response['Content-Security-Policy'] = "default-src 'self' frame-ancestors http://localhost:3000 http://localhost:3000/ *"
        return response
        # return Response({"data":"filex.read()"},status.HTTP_200_OK)