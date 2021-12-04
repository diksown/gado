# gado

**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs errors and warnings in poetry format.

## Usage

After installing, you will be able to call gado and gado++. You can use them just like gcc/g++!

Type `gado --help` for more info.

Examples:

```
gado source.c -Wall -o output_executable
gado++ source.cpp -Wall -o output_executable
```

**Tip:** There is a `errors.cpp` on the `test` folder. Why don't you try to compile it with `gado++ errors.cpp`?

**TODO:** Put some images

## Installing

You need GCC 9, Python3 and pip in order to install gado.

To intall:

```
git clone https://github.com/diksown/gado
cd gado
sudo ./setup.sh install
```
