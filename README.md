<p align="center"><img src="https://user-images.githubusercontent.com/49994083/144731656-29900b63-7824-4077-b109-9a771af67e38.png" width="500px"></p>
<h1 align="center">gado</h1>
<p align="center">make poetry with gcc diagnostics</p>

### 🪶 About 

**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs its errors and warnings in a more poetic format.

It currently takes rhymes from a database of all Shakespeare's works.

### 🔎 Usage 

After installing, you will be able to call `gado` and `gado++`. You can use them just like `gcc/g++`!

**Examples:**

```
gado source.c -Wall -o output_executable
gado++ source.cpp -Wall -o output_executable
```

**💡 Tip:** There is a `errors.cpp` on the `test` folder. Why don't you try to compile it with `gado++ errors.cpp`?

Type `gado --help` for more info.

### 📝 Requirements
You need gcc 9, python3 and pip in order to install gado.

### ⬇️ Installing
```
git clone https://github.com/diksown/gado
cd gado
sudo ./setup.sh install
```
