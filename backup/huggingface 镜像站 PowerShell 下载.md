 AI开发绕不过一个问题是，如何从hugging face下载模型/数据集，其实网络快、稳的话，随便哪种方法都挺好，然而国内网络问题，断点续传、多线程下载 等特性就显得尤为必要了，否则动辄断掉重来、下载速度慢，浪费生命！基于这个考虑，本文集成官方方法、第三方奇技淫巧，做了个总结排序

- https://hf-mirror.com/
- https://gist.github.com/padeoe/697678ab8e528b85a2a7bddafea1fa4f
- https://padeoe.com/huggingface-large-models-downloader/
-

### 下载对比

| 方法类别 | 示例 / 链接 | 推荐程度 | 优点 | 缺点 |
|-----------|--------------|------------|--------|--------|
| 基于URL | [浏览器网页下载](https://padeoe.com/huggingface-large-models-downloader/#1.-%E6%B5%8F%E8%A7%88%E5%99%A8%E7%BD%91%E9%A1%B5%E4%B8%8B%E8%BD%BD) | ⭐⭐⭐ | 通用性好 | 手动麻烦 / 无多线程 |
| 多线程下载器 | [多线程下载器](https://padeoe.com/huggingface-large-models-downloader/#2.-%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%B8%8B%E8%BD%BD%E5%99%A8) | ⭐⭐⭐⭐ | 通用性好 | 手动麻烦 |
| CLI工具 | [git clone 命令](https://padeoe.com/huggingface-large-models-downloader/#3.-Git-clone) | ⭐⭐ | 简单 | 无断点续传 / 冗余文件 / 无多线程 |
| 专用CLI工具 | [huggingface-cli + hf_transfer](https://padeoe.com/huggingface-large-models-downloader/#4.-huggingface-cli%2Bhf_transfer) | ⭐⭐⭐ | 官方下载工具链，功能最全 | 无进度条 / 容错性低 |
| huggingface-cli | [huggingface-cli](https://padeoe.com/huggingface-large-models-downloader/#4.1-huggingface-cli) | ⭐⭐⭐⭐⭐ | 官方下载工具 | 不支持多线程 |
| Python方法 | [snapshot_download](https://padeoe.com/huggingface-large-models-downloader/#5.-snapshot_download) | ⭐⭐⭐ | 官方支持，功能全 | 脚本复杂 / 无多线程 |
| from_pretrained | [from_pretrained](https://padeoe.com/huggingface-large-models-downloader/#6.-from_pretrained) | ⭐ | 官方支持，简单 | 不方便存储 / 功能不全 |
| hf_hub_download | [hf_hub_download](https://padeoe.com/huggingface-large-models-downloader/#6.-hf_hub_download) | ⭐ | 官方支持 | 不支持全量下载 / 无多线程 |



### 安装依赖

打开 PowerShell 安装依赖
```
pip install -U "huggingface_hub[cli]"
```

如失败卸载安装稳定版本
```
pip uninstall -y huggingface_hub
pip install huggingface_hub==0.25.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装依赖
```
dir "D:\Python313\Scripts" | findstr huggingface
```

一般输出
```
-a----         2025/11/1  ?? 11:54         108371 huggingface-cli.exe
```

### 下载数据集
```
$env:HF_ENDPOINT = "https://hf-mirror.com"
& "D:\Python313\Scripts\huggingface-cli.exe" download --repo-type dataset --resume-download datxy/file --local-dir D:\hf2\datxy_file --local-dir-use-symlinks False
```