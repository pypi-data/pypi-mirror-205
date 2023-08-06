# uphill
[![Python-Version](https://img.shields.io/badge/Python-3.7%7C3.8-brightgreen)](https://aigit.huya.com/xuyinan/uphill)

Easy to process and store data.

## install
```
pip3 install git+https://aigit.huya.com/xuyinan/uphill
```

## Document
We afford python package and bin mode. For more details, please check `uphill -h`. 
```
usage: uphill [-h] [-v] {download,prepare} ...

MountainTop Line Interface

optional arguments:
  -h, --help          show this help message and exit
  -v, --version       show UpHill version

subcommands:
  use "uphill [sub-command] --help" to get detailed information about each sub-command

  {download,prepare}
    download          👋 download a dataset automatically
    prepare           👋 prepare a dataset automatically

uphill v0.0.1, a toolkit based on pytorch. Visit https://github.com/yinanxu0/uphill for tutorials and documents.
```
For convenience, you can use `uh` instead of `uphill`, like `uh -h`.

### Download dataset
For example, download Aishell dataset
```
uh download --dataset aishell --target_dir ${download_dir}
```

More details of parameters in help mode.
```
uh download -h
```


### Prepare dataset
```
uh prepare --dataset aishell --corpus_dir ${download_dir}/aishell --target_dir ${data_dir} --num_jobs 8 --compress

```
