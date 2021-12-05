# gado 🐮


```
I know I love in vain, strive against hope;  
‘totalTimeSpent’ was not declared in this scope
```
**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs its errors and warnings in a more poetic format.


### Usage 🔎

After installing, you will be able to call `gado` and `gado++`. You can use them just like `gcc/g++`!

**Examples:**

```
gado source.c -Wall -o output_executable
gado++ source.cpp -Wall -o output_executable
```

**💡 Tip:** There is a `errors.cpp` on the `test` folder. Why don't you try to compile it with `gado++ errors.cpp`?

Type `gado --help` for more info.

### Requirements
You need GCC 9, Python3 and pip in order to install gado.

### Installing
```
git clone https://github.com/diksown/gado
cd gado
sudo ./setup.sh install
```
