# ScriptVideoCreator

字幕音视频生成器  

[项目的详细说明](https://smacul.github.io/log/script_with_voice/)

这个生成器读取台词后, 利用 Google Text-to-Speech 生成音频, 利用 PIL 以及 opencv 生成字幕视频, 最终输出所有台词的音视频. 具体效果可以参考 result.mp4

## 使用
1. 申请一个 google Text-to-Speech API 的使用账号.
1. 编写 audioScript.txt 与 wordScript.txt 两个文件.
1. 视情况修改 Main.py 中的内容
1. 运行 Main.py
