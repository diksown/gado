<p align="center"><img src="https://user-images.githubusercontent.com/49994083/144793848-685e313b-1e61-4c60-8baf-3b59574f2706.png"></p>

<h1 align="center">gado</h1>
<p align="center">generate poetry with gcc diagnostics</p>

## 🖋️ About 

**gado** (**g**cc **a**wesome **d**iagnostics **o**rchestrator) is a wrapper of gcc that outputs its errors and warnings in a more poetic format.

It currently takes rhymes from a database of all Shakespeare's works.

## 🔎 Usage 

After installing, you will be able to call `gado` and `gado++`. You can use them just like `gcc/g++`!

**Examples:**

```
gado source.c -Wall -o output_executable
gado++ source.cpp -Wall -o output_executable
```

**💡 Tip:** There is a `errors.c` on the `test` folder. Why don't you try to compile it with `gado errors.c`?

Type `gado --help` for more info.

## 📝 Requirements

You need gcc>=9, python3 and pip in order to install gado.

## ⬇️ Installing

### PyPI

As gado is written in python, installation by pip is recommended.

```
pip install gado
```

### Manual

You can manually install gado by cloning this repository and running `setup.py`.

```
git clone https://github.com/diksown/gado
cd gado
python setup.py install --force
```

## 🤝 Contributing

**gado** is open source. You are more than welcome to [help on it](https://github.com/diksown/gado/issues)!
