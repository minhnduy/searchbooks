# TVTTDPT2018_2019_16521735_16521703_16521688
Đồ án cuối kì môn truy vấn thông tin đa phương tiện 2018 - 2019

## Get started

- Install [Python 3.5+](https://www.python.org/)
- Install [NLTK 3](http://www.nltk.org/) package via `pip` command:

```bash
$ pip install nltk
```

## Usage

Run `index.py` script to index documents stored in `resources/dataset` directory:

```bash
$ python index.py
```

The indexed data is stored in `data/` directory. The set of words is stored in `dictionary.txt` file.
The list of all documents and inverted index is serialized into `docs.pickle` and `inverted_index.pickle` files (using `pickle` serializer module). These files will be read by `query.py` script to perform query.

To perform query, run `query.py` script and provide an argument for it:

```bash
$ python query.py "your query here"
```
