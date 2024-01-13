from django.db import models






class PegawaiModel(models.Model):
    id_pegawai  =models.BigAutoField(primary_key=True)
    nama  = models.CharField(max_length=20)
    departemen = models.CharField(max_length=10)
    class Meta:
        db_table='pegawai'


class PerusahaanModel(models.Model):
    id_perusahaan = models.BigAutoField(primary_key=True)
    nama_pelakuUsaha = models.CharField(max_length=20, blank=True, null=True)
    nama_pbphh = models.CharField(max_length=20, blank=True, null=True)
    kbli = models.CharField(max_length=20, blank=True, null=True)
    nib = models.CharField(max_length=20, blank=True, null=True)
    npwp = models.CharField(max_length=20, blank=True, null=True)
    alamat_kantor = models.CharField(max_length=50, blank=True, null=True)
    alamat_usaha = models.CharField(max_length=50, blank=True, null=True)
    alamat_gudang = models.CharField(max_length=50, blank=True, null=True)
    jenis_produk = models.CharField(max_length=100, blank=True, null=True)
    daftar_mesin = models.CharField(max_length=100, blank=True, null=True)
    sumber_bahan = models.CharField(max_length=20, blank=True, null=True)
    total_investasi = models.IntegerField(blank=True, null=True)
    status_permohonan = models.CharField(max_length=15)
    jumlah_tenaga_kerja = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'perusahaan'

class PermohonanModel(models.Model):
    id_request = models.BigAutoField(primary_key=True)
    id_perusahaan = models.ForeignKey(PerusahaanModel, on_delete=models.SET_NULL ,null=True)
    id_pegawai = models.ForeignKey(PegawaiModel, on_delete=models.SET_NULL ,null=True)
    sub_date = models.DateField(auto_created=False,auto_now_add=False,auto_now=False)
    skala  =models.CharField(max_length=15)
    status_permohonan = models.CharField(max_length=10)
    readTrue = models.BooleanField(default=False,null=True,blank=True)
    posisi = models.CharField(max_length=15)
    class Meta:
        db_table = 'permohonan'

class DokumenModel(models.Model):
    id_dokumen = models.BigAutoField(primary_key=True)
    id_permohonan = models.ForeignKey(PermohonanModel,on_delete=models.SET_NULL,null=True)
    nama_dokumen = models.CharField(max_length=75)
    tipe_dokumen = models.CharField(max_length=5)
    dokumen_path = models.CharField(max_length=75)
    read_true = models.BooleanField(default=False,null=True,blank=True)
    note = models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        db_table = 'dokumen'

