# 基于[g729a-python](https://github.com/AlexIII/g729a-python)的G.729编解码工具

本项目基于g729a-python，对wav与G.729音频格式的转换提供了函数封装。

提供了 **Python脚本直接运行** 与 **命令行调用** 两种使用方式。

- **Python脚本**

  `python/g729a.py`：提供了`convert_wav_to_g729`和`convert_g729_to_wav`两个编解码API。

  `python/example.py`：根据提供了转换前后音频文件路径，可直接运行的示例脚本。

- **命令行调用**

  `bin`文件夹下自行编制bat文件。文件内容示例为：

  ```sh
  @echo off  
  python path/to/g729a.py %*
  ```

  根据需要将g729a.bat设置为系统环境变量。(Linux与windows环境均适用)

  命令行调用指令：

  ```
  g729a encode/decode in_file out_file
  ```

  其中  **encode** 和 **decode** 分别负责将wav文件编码为G.729格式，和对G.729格式音频进行解码。

