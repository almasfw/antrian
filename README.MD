# Antrian dan Simulasi

_Submission_ tugas mata kuliah Antrian dan Simulasi (MII4213) Semester Genap 2019/2020

Oleh:

- Almas Fauzia Wibawa
- Gregorius Aria Neruda
- Rayhan Naufal Ramadhan

## Eksekusi Program

- M/M/1/K

```
$ python ./MM1K.py -K
```

Di mana `K` adalah maksimal banyaknya _customer_ di dalam antrian (termasuk yang sedang di-_serve_)

- M/M/c/K

```
$ python ./MMcK.py -c -K
```

Di mana `c` adalah banyaknya server di dalam antrian, dan `K` adalah maksimal banyaknya _customer_ di dalam antrian (tidak termasuk yang sedang di-_serve_)

- n\*M/M/1/K

```
$ python ./n-MM1K.py -n -K
```

Di mana `n` adalah banyaknya antrian M/M/1, dan `K` adalah maksimal banyaknya _customer_ di dalam antrian (tidak termasuk yang sedang di-_serve_)
