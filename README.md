# roborecipe

## Abstruct
RoboRecipe generate Assembly instructions automatically.  
See [Generated html file](https://eriac.github.io/roborecipe/).

## framework
roborecipe is no Python3, and target OS is Ubuntu20.4

# usage

## how to install
```code
$ git clone git@github.com:eriac/roborecipe.git  
$ cd roborecipe
$ pip install ./ (add -e for develope mode)
```

## how to use
```code
$ roborecipe # dispaly help
```

## generate instruction with sample
```code
$ roborecipe list -d ~/roborecipe/sample/ 
### package ###
...
### component ###
...
```

## how to uninstall
```code
pip uninstall roborecipe
```
