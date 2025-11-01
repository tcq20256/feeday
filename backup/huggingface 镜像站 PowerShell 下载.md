

打开 PowerShell 安装依赖
```
pip install -U "huggingface_hub[cli]"
```

如失败卸载安装稳定版本
```
pip uninstall -y huggingface_hub
pip install huggingface_hub==0.25.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

设置镜像环境变量
```
$env:HF_ENDPOINT = "https://hf-mirror.com"
```

确认 Python 安装目录
```
D:\Python313\
```

下载数据集
```
$env:HF_ENDPOINT = "https://hf-mirror.com"
& "D:\Python313\Scripts\huggingface-cli.exe" download --repo-type dataset --resume-download datxy/file/ --local-dir D:\hf_downloads\datxy_file --local-dir-use-symlinks False
```