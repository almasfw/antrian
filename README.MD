# Antrian dan Simulasi

_Submission_ tugas mata kuliah Antrian dan Simulasi (MII4213) Semester Genap 2019/2020

Oleh:

- Almas Fauzia Wibawa
- Gregorius Aria Neruda
- Rayhan Naufal Ramadhan

## Implementasi

Di dalam folder ini terdapat 3 simulator untuk 3 permasalahan yang berbeda, yaitu:
- Permasalahan antrian M/M/1/K
- Permasalahan antrian M/M/c/K
- Permasalahan antrian n-M/M/1/K

Ketiga permasalahan tersebut diselesai dengan implementasi berbasis event. Terdapat 2 jenis event, arrival dan service. Event dengan rate yang paling kecil akan dieksekusi lebih dulu.

1) Yang terjadi ketika event arrival dieksekusi adalah datangnya customer baru ke dalam sistem. Event arrival yang baru saja dieksekusi kemudian dihapus dan dibuat event arrival baru dengan rate random. Rate pada event arrival baru menandakan waktu yang dibutuhkan untuk customer selanjutnya tiba di sistem.

2) Yang terjadi ketika event service dieksekusi adalah perginya seorang customer dari sistem. Event service yang baru saja dieksekusi dihapus dan dibuat event service baru dengan rate random. Rate pada event service baru menandakan waktu yang dibutuhkan server untuk melayani customer selanjutnya.

Dalam merandom rate, digunakan exponential distribution (CDF) dengan lambda 0,5. Nilai lambda dapat diubah dengan mengganti nilai exp_dist_lambda pada program.

Log yang dihasilkan menyimpan informasi mengenai:
1) Kedatangan customer.
2) Masuknya customer ke server.
3) Kepergian customer.
4) Dilakukannya drop ketika customer datang dan antrian telah penuh.
Masing-masing informasi akan disertai dengan timestamp untuk menunjukkan pada detik ke berapa peristiwa tersebut terjadi.

## Eksekusi Program

Untuk menjalankan program, silakan membuka bash pada direktori disimpannya program. Untuk masing-masing program, silakan jalankan perintah:

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