# roborecipe

## Abstruct
RoboRecipe generate Assembly instructions automatically.  
See [Generated html file](https://eriac.github.io/roborecipe/).


## how to use
$ git clone git@github.com:eriac/roborecipe.git  
$ cd roborecipe  
$ python make_image.py  
$ python make_html.py  

## files
- make_html.py  
htmlファイル(index.html)を作成するプログラムです。
- make_image.py  
gif画像(image/)を作成するプログラムです。
- stl_load.py  
stlファイルを読み込むためのライブラリです。
- xml_load.py  
xmlのパースをするプログラム
- data.xml  
組み立ての構造を記述するxmlファイルです。
- **.stl  
部品の外形を記述しているstlファイルです。


