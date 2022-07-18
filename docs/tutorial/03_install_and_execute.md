# install & execute

## install 
pipを使ってインストールできます。

```code
pip install roborecipe

```

正常にインストールされればroborecipeコマンドが使えます。

```code
$ roborecipe
usage: roborecipe [-h] [-d DIRECTORY] [-o OUTPUT] [-t] command [option [option ...]]
roborecipe: error: the following arguments are required: command
```

## execute
generateコマンドで引数でほしい組み立てずの対象のアセンブリコンポーネントの名前を指定します。ここではsample_projectプロジェクトのmain_asmアセンブルコンポーネントを指定します。
オプションでサーチディレクトリと出力ファイルのディレクトリを指定できます。


```code
roborecipe generate sample_project main_asm -d {サーチディレクトリ} -o {出力ディレクトリ}
```
