# roborecipe

## Abstruct
RoboRecipe generate Assembly instructions automatically.  
See [Generated html file](https://eriac.github.io/roborecipe/sample_out).

## framework
roborecipe is no Python3, and target OS is Ubuntu20.4

# file refference

see [xml document](doc/xml_reference.md)

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

## get list of component with sample 
```code
$ roborecipe list -d ~/roborecipe/sample/ 
### package ###
...
### component ###
...
```

## generate instruction with sample
```code
$ roborecipe generate sample_project main_asm -d roborecipe/sample/ -o out
```

## how to uninstall
```code
pip uninstall roborecipe
```
