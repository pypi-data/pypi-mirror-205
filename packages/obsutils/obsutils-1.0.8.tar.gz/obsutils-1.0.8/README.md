# obsutils

#### 介绍
华为modelarts对象存储的下载工具，MoXing的替代品

#### 安装

pip install obsutils -i https://pypi.tuna.tsinghua.edu.cn/simple

#### 使用说明

```python
import obsutils

obsutils.init('ak', 'sk', 'endpoint') # 如果在平台上使用，可以不用初始化
obsutils.copy('obs://bucket/key', 'local_path')
```

#### 注意

目前仅支持从obs下载目录到本地，不支持下载单个文件，也不支持上传