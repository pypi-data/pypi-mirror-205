# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bilifan',
 'nonebot_plugin_bilifan.login',
 'nonebot_plugin_bilifan.src']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-socks>=0.8.0,<0.9.0',
 'aiohttp>=3.8.3,<4.0.0',
 'nonebot-adapter-onebot>=2.1.5',
 'nonebot2>=2.0.0rc4,<3.0.0',
 'nonebot_plugin_apscheduler>=0.2.0',
 'pillow>=9.3.0,<10.0.0',
 'pyyaml>=6.0,<7.0',
 'qrcode>=7.4.2,<8.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bilifan',
    'version': '0.1.2',
    'description': '刷bili粉丝牌子的机器人插件',
    'long_description': '<div align="center">\n  <img src="https://raw.githubusercontent.com/Agnes4m/nonebot_plugin_l4d2_server/main/image/logo.png" width="180" height="180"  alt="AgnesDigitalLogo">\n  <br>\n  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot_plugin_bilifan\n_✨自动b站粉丝牌✨_\n\n<a href="https://github.com/Agnes4m/nonebot_plugin_bilifan/stargazers">\n        <img alt="GitHub stars" src="https://img.shields.io/github/stars/Agnes4m/nonebot_plugin_bilifan" alt="stars">\n</a>\n<a href="https://github.com/Agnes4m/nonebot_plugin_bilifan/issues">\n        <img alt="GitHub issues" src="https://img.shields.io/github/issues/Agnes4m/nonebot_plugin_bilifan" alt="issues">\n</a>\n<a href="https://jq.qq.com/?_wv=1027&k=HdjoCcAe">\n        <img src="https://img.shields.io/badge/QQ%E7%BE%A4-399365126-orange?style=flat-square" alt="QQ Chat Group">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot_plugin_bilifan">\n        <img src="https://img.shields.io/pypi/v/nonebot_plugin_bilifan.svg" alt="pypi">\n</a>\n    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n    <img src="https://img.shields.io/badge/nonebot-2.0.0rc4-red.svg" alt="NoneBot">\n</div>\n\n\n## 配置\n\n启动一次插件，在bot路径下，"data/bilifan"文件夹内，按需求修改"users.yaml"文件\n\n## 指令\n\n - b站登录 - 返回b站二维码，扫码登录，绑定qq号\n - 开始刷牌子 - 开始执行命令\n - 自动刷牌子 - 添加或取消定时任务\n - 删除全部刷牌子 - [超管]删除全部的定时任务\n\n\n</details>\n\n## 🙈 其他\n\n+ 如果本插件对你有帮助，不要忘了点个Star~\n+ 本项目仅供学习使用，请勿用于商业用途\n+ [爱发电](https://afdian.net/a/agnes_digital)\n+ [GPL-3.0 License](https://github.com/Agnes4m/nonebot_plugin_bilifan/blob/main/LICENSE) ©[@Agnes4m](https://github.com/Agnes4m)\n        \n\n## 🌐 感谢\n\n- [新 B 站粉丝牌助手](https://github.com/XiaoMiku01/fansMedalHelper) - 源代码来自于他\n',
    'author': 'Agnes_Digital',
    'author_email': 'Z735803792@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Agnes4m/nonebot_plugin_l4d2_server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
