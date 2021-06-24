# ZJU Console Gamer

支持7党，反对17

[ZJU Console Gamer](https://www.zjuconsole.xyz/)


## 经常会被问到的问题

* 为什么我不能编辑网页

因为这是一个静态网站，所有的内容都基于已经存在的excel文件。这意味着所有的内容更新都基于excel文件的更新，也就是我每次手动从腾讯文档上导出然后传到github上。想要直接从网站上更新，需要的工作量太大，同时也需要平衡群友使用时候的易用性，在可以预见的未来中是不会实现这个功能的。

* 为什么有的地方标题看起来不太对

九成九是因为excel表格中输入的格式不对。如果有发现可以通知学姐。

* 学姐是谁

是群主，是17。

* 如何在本地构建、开发、调试此项目

参考GitHub Action的构建流程。

```
git clone git@github.com:schwarzichet/schwarzichet.github.io.git
pip install -r requirements.txt
python readexcel.py
npm install

# build
npm run docs:build

# dev
npm run docs:dev
```
本项目基于vuepress 2.0。

* 为什么没有XX，XX，XX功能，为什么XX这么丑

欢迎PR，诚招前端工程师。你可以在群里提需求，但是我不一定会响应，只能视心情决定。







