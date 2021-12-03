# gado

**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs errors and warnings in poetry format.

## Usage

After installing, you will have gado and gado++. You can use them as you would do with gcc/g++.

Type `gado --help` for more info.

Examples:
```
gado++ main.cpp -o main
gado main.c -o main
```

**TODO:** Put some images

## Installing

You need GCC 9 and Python 3 in order to install gado.

```
git clone https://github.com/diksown/gado
cd gado
sudo ./setup.sh install
```
