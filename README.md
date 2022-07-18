# Roborecipe

## Abstruct
Roborecipe generate robot build instructions automatically.  
See [Generated html file](https://eriac.github.io/roborecipe/docs/sample_out).

## framework
roborecipe is based on Ubuntu20.4 and Python3

# source file reference
see [xml document](https://github.com/eriac/roborecipe/blob/master/docs/xml_reference.md)

# usage

## how to install

### from PyPl (pip)
```code
pip install roborecipe

```

### from source
```code
$ git clone https://github.com/eriac/roborecipe.git  
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
