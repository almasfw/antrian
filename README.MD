# Antrian dan Simulasi

Submisi tugas mata kuliah Antrian dan Simulasi (MII4213) Semester Genap 2019/2020
Program Studi Ilmu Komputer
Departemen Ilmu Komputer dan Elektronika
Fakultas Matematika dan Ilmu Pengetahuan Alam
Universitas Gadjah Mada

Oleh:

- Almas Fauzia Wibawa
- Gregorius Aria Neruda
- Rayhan Naufal Ramadhan

## Implementasi

Di dalam folder ini terdapat 3 simulator untuk 3 permasalahan yang berbeda, yaitu:
- Permasalahan antrian M/M/1/K
- Permasalahan antrian M/M/c/K
- Permasalahan antrian n-M/M/1/K

Ketiga permasalahan tersebut diselesaikan dengan implementasi berbasis _event_. Terdapat 2 jenis _event_, _arrival_ dan _service_. _Event_ dengan _rate_ yang paling kecil akan dieksekusi lebih dulu.

1) Yang terjadi ketika _event arrival_ dieksekusi adalah datangnya _customer_ baru ke dalam sistem. _Event arrival_ yang baru saja dieksekusi kemudian dihapus dan dibuat _event arrival_ baru dengan _rate random_. _Rate_ pada _event arrival_ baru menandakan waktu yang dibutuhkan untuk _customer_ selanjutnya tiba di sistem.

2) Yang terjadi ketika _event service_ dieksekusi adalah perginya seorang _customer_ dari sistem. _Event service_ yang baru saja dieksekusi dihapus dan dibuat _event service_ baru dengan _rate random_. _Rate_ pada _event service_ baru menandakan waktu yang dibutuhkan server untuk melayani _customer_ selanjutnya.

Dalam me-_random rate_, digunakan _exponential distribution_ (CDF) dengan lambda 0,5. Nilai lambda dapat diubah dengan mengganti nilai exp_dist_lambda pada program.

Log yang dihasilkan menyimpan informasi mengenai:
1) Kedatangan _customer_.
2) Masuknya _customer_ ke server.
3) Kepergian _customer_.
4) Dilakukannya drop ketika _customer_ datang dan antrian telah penuh.

Masing-masing informasi akan disertai dengan _timestamp_ untuk menunjukkan pada detik ke berapa peristiwa tersebut terjadi.

## Eksekusi Program

Untuk menjalankan program, eksekusi _commmand line_ di bawah ini pada direktori disimpannya program:

1) M/M/1/K

```
$ python ./MM1K.py -K
```

Di mana `K` adalah maksimal banyaknya _customer_ di dalam antrian (termasuk yang sedang di-_serve_)

Akan dihasilkan log dengan nama file logMM1K.csv setelah program selesai dijalankan.

2) M/M/c/K

```
$ python ./MMcK.py -c -K
```

Di mana `c` adalah banyaknya server di dalam antrian, dan `K` adalah maksimal banyaknya _customer_ di dalam antrian (tidak termasuk yang sedang di-_serve_)

Akan dihasilkan log dengan nama file logMMcK.csv setelah program selesai dijalankan.

3) n-M/M/1/K

```
$ python ./n-MM1K.py -n -K
```

Di mana `n` adalah banyaknya antrian M/M/1, dan `K` adalah maksimal banyaknya _customer_ di dalam antrian (tidak termasuk yang sedang di-_serve_)

Akan dihasilkan log dengan nama file logN-MM1K.csv setelah program selesai dijalankan.