# libraries
## argparse
* -d target_directory
* -o output_directory
* command
    * list
    * tree
    * generate
    * show

## pyinstaller

https://kazuhira-r.hatenablog.com/entry/2019/04/25/002033

# test install
pip install -e .

# wheel
refer https://qiita.com/propella/items/803923b2ff02482242cd

## generate wheel pkg
`python3 setup.py bdist_wheel`

roborecipe-0.0.1-py3-none-any.whl is generated

## install
pip install ../packaging_tutorial/dist/corona_propella-0.0.1-py3-none-any.whl

## architecture
list - list of item
tree - tree of relation
quantity - list of quantity
order - list of dependency

package/component
->
list - list of component in all packages

+ target component
tree get tree
quantity get quantity list
order get dependency tree

instruction

-> header part

-> purchase part
- list
- quantity

-> preparation part
- order

-> assembly part
- order

## instruction

* purchase(table)
    * pkg/item name
    * quantity
    * price
    * seller
    * desctiption

* preparation
* each(list)
    * pkg/item name
    * require_quantity
    * description
    * step(list)
        * source(list)
            * pkg/item name
            * quantity
        * picture
        * description

* assembly
* each(list)
    * pkg/item name
    * require_quantity
    * description
    * step(list)
        * source(list)
            * pkg/item name
            * quantity
        * picture
        * description

# class
* data_geter -> component_list_data
* data_process
* image_generator
* html_generator

# activity

```plantuml
start
:directory search;
:parse component;
end
```