

<p align="center"><img src="https://user-images.githubusercontent.com/49994083/146096949-671b2608-664a-4471-ac4b-7f3510ad6bde.png"></p>


<h1 align="center">gado</h1>
<p align="center">
  generate poetry with gcc diagnostics
</p>

## 🖋️ About 

**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs its errors and warnings in a more poetic format.

You can see [some examples on its website](https://gado.dikson.xyz)!

It currently takes rhymes from a database of all Shakespeare's works.

## 🔎 Usage 

After installing, you will be able to call `gado` and `gado++`. You can use them just like `gcc/g++`!

Type `gado --help` for more info.

**Examples:**

```
gado source.c -o executable
gado++ source.cpp -o executable
```

**💡 Tip:** There are `C/C++` source files in the `examples` folder. Why don't you try to compile them (with `gado errors.c` or `gado++ errors.cpp`)?


## 📝 Requirements

You need gcc>=9, python3 and pip in order to install gado.

## ⬇️ Installing

### PyPI

As gado is written in python, installation by pip is recommended.

```
sudo pip install gado
```

### Manual

You can manually install gado by cloning this repository and running the install script.

```
git clone https://github.com/diksown/gado
cd gado
sudo python setup.py install
```

## 🤝 Contributing

**gado** is open source. You are more than welcome to [help on it](https://github.com/diksown/gado/issues)!
