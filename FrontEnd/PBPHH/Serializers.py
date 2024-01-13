from django.template.defaultfilters import default
from rest_framework import serializers

from FrontEnd.PBPHH.models import PegawaiModel, PermohonanModel, PerusahaanModel, DokumenModel


class PegawaiSerializer(serializers.Serializer):
    id_pegawai  = serializers.IntegerField(required=False)
    nama  = serializers.CharField(max_length=20)
    departemen = serializers.CharField(max_length=10)
    class Meta:
        model = PegawaiModel
        exclude = []

    def create(self, validated_data):
        data = PegawaiModel.objects.create(**validated_data);
        return data


class PerusahaanSerializer(serializers.Serializer):
    id_perusahaan = serializers.IntegerField(required=False)
    nama_pelakuUsaha = serializers.CharField(max_length=20)
    nama_pbphh = serializers.CharField(max_length=20)
    kbli = serializers.CharField(max_length=20)
    nib = serializers.CharField(max_length=20)
    npwp = serializers.CharField(max_length=20)
    alamat_kantor = serializers.CharField(max_length=50)
    alamat_usaha = serializers.CharField(max_length=50)
    alamat_gudang = serializers.CharField(max_length=50)
    # jenis_produk = serializers.ListField(child=serializers.ListField(),source="jenis_produk",required=False,allow_empty=True)
    # daftar_mesin = serializers.ListField(child=serializers.ListField(),source="daftar_mesin",required=False,allow_empty=True)
    # jenis_produk_kecil = serializers.ListField(source="jenis_produk",child=serializers.CharField(max_length=100), write_only=True,required=False,allow_null=True,allow_empty=True)
    # daftar_mesin_kecil = serializers.ListField(source="daftar_mesin",child=serializers.CharField(max_length=100), write_only=True,required=False,allow_null=True,allow_empty=True)
    jenis_produk = serializers.CharField(max_length=100)
    daftar_mesin = serializers.CharField(max_length=100)
    sumber_bahan = serializers.CharField(max_length=20)
    total_investasi = serializers.IntegerField( )
    status_permohonan = serializers.CharField(max_length=15)
    jumlah_tenaga_kerja = serializers.IntegerField()
    class Meta:
        model = PerusahaanModel
    def create(self, validated_data):
        # print(validated_data)

        response = PerusahaanModel.objects.create(**validated_data)
        print("response",response.daftar_mesin)
        return response
    def update(self, instance, validated_data):
        instance.nama_pelakuUsaha = validated_data["nama_pelakuUsaha"]
        instance.nama_pbphh = validated_data["nama_pbphh"]
        instance.kbli = validated_data["kbli"]
        instance.nib = validated_data["nib"]
        instance.npwp = validated_data["npwp"]
        instance.alamat_kantor = validated_data["alamat_kantor"]
        instance.alamat_usaha = validated_data["alamat_usaha"]
        instance.alamat_gudang = validated_data["alamat_gudang"]
        instance.jenis_produk = validated_data["jenis_produk"];
        instance.daftar_mesin = validated_data["daftar_mesin"];
        instance.sumber_bahan = validated_data["sumber_bahan"]
        instance.total_investasi = validated_data["total_investasi"]
        instance.status_permohonan = validated_data["status_permohonan"]
        instance.jumlah_tenaga_kerja = validated_data["jumlah_tenaga_kerja"]
        instance.save()
        return instance

class DokumenSerializer(serializers.Serializer):
    id_dokumen = serializers.IntegerField(required=False)
    id_permohonan = serializers.PrimaryKeyRelatedField(queryset=PermohonanModel.objects.all(),required=False,allow_empty=True,allow_null=True)
    nama_dokumen = serializers.CharField(max_length=75)
    tipe_dokumen = serializers.CharField(max_length=5)
    dokumen_path = serializers.CharField(max_length=75)
    read_true = serializers.BooleanField()
    note = serializers.CharField(max_length=250,allow_null=True,allow_blank=True)
    class Meta:
        db_table = DokumenModel
        exclude = []
    def create(self, validated_data):
        resp = DokumenModel.objects.create(**validated_data)
        return resp
    def update(self, instance, validated_data):
        instance.nama_dokumen = validated_data["nama_dokumen"]
        instance.tipe_dokumen = validated_data["tipe_dokumen"]
        instance.dokumen_path = validated_data["dokumen_path"]
        instance.read_true = validated_data["read_true"]
        instance.note = validated_data["note"]
        instance.save()
        return instance
class DokumenSerializers(serializers.Serializer):
    nama_dokumen = serializers.CharField(max_length=20)
    class Meta:
        db_table = DokumenModel

        fields = ("nama_dokumen")
    def create(self, validated_data):
        resp = DokumenModel.objects.create(**validated_data)
        return resp
    def update(self, instance, validated_data):
        instance.nama_dokumen = validated_data["nama_dokumen"]
        instance.tipe_dokumen = validated_data["tipe_dokumen"]
        instance.dokumen_path = validated_data["dokumen_path"]
        instance.read_true = validated_data["read_true"]
        instance.note = validated_data["note"]
        instance.save()
        return instance
class PermohonanSerializer(serializers.Serializer):
    id_request = serializers.IntegerField(required=False)
    perusahaan = PerusahaanSerializer(source='id_perusahaan',read_only=True)
    dokumen = DokumenSerializer(source='dokumenmodel_set', many=True, read_only=True)
    id_perusahaan = serializers.PrimaryKeyRelatedField(queryset=PerusahaanModel.objects.all(),write_only=True, required=False)
    id_pegawai = serializers.PrimaryKeyRelatedField(queryset=PegawaiModel.objects.all(),required=False)
    sub_date = serializers.DateField(format="%d-%m-%Y",allow_null=True,required=False)
    skala  =serializers.ChoiceField(choices=("Besar","Kecil"))
    status_permohonan = serializers.CharField(max_length=10)
    posisi = serializers.ChoiceField(choices=("fd","pb","kabid_phpl","kadis"))
    readTrue = serializers.BooleanField()
    class Meta:
        db_table = PermohonanModel
        exclude = []
    def update(self, instance, validated_data):
        instance.id_pegawai= validated_data["id_pegawai"]
        instance.sub_date= validated_data["sub_date"]
        instance.skala= validated_data["skala"]
        instance.status_permohonan= validated_data["status_permohonan"]
        instance.posisi=validated_data["posisi"]
        instance.readTrue= validated_data["readTrue"]
        instance.save()
        return instance
    def create(self, validated_data):
        response = PermohonanModel.objects.create(**validated_data)

        # print(validated_data)
        # serial = PerusahaanSerializer(data=validated_data['Perusahaan'])
        # serial.is_valid(raise_exception=True)
        # serial.save()
        # validated_data['Permohonan'] = serial['id_pegawai']
        # print(serial,"\n",validated_data)
        # response = PermohonanModel.objects.create(**validated_data['Permohonan'])
        # for e in validated_data['Dokumen']:
        #     e['id_permohonan'] = response['id_request']
        # serial2 = DokumenSerializer(data=validated_data['Dokumen'], many=True)
        # serial2.is_valid(raise_exception=True)
        # serial2.save()
        # print(validated_data)
        return response
