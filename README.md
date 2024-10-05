<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-BF5-grouptools
</div>
本插件可以实现验证 BF5 账号是否属实，如果属实即自动批准入群并修改其群名片为申请时输入的 ID。

请在使用时通过 `管理群` -> `加群方式` -> `需要身份认证` 中开启 `需要回答问题并由管理员审核` 并将机器人账号设为管理员。


## 安装
* 使用pip 
```
pip install nonebot_plugin_BF5_grouptools
```
并在bot根目录的`pyproject.toml`文件中加入  
```
plugins = ["nonebot_plugin_BF5_grouptools"]
```


* 使用 nb_cli（推荐）
```
nb plugin install nonebot_plugin_BF5_grouptools
```


## 鸣谢

> 本插件修改自 [nonebot-plugin-bf1-groptools](https://github.com/qienoob/nonebot_plugin_bf1_groptools)
