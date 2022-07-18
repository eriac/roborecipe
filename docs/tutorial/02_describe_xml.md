# target
このページではパッケージファイル、部品/アセンブルコンポーネントファイルの書き方を説明します。

# package file
ルート要素は<package>です。子要素のname要素でpackage名を決めます。
ディレクトリ名ではなく、xml中に記載したものがpackage名となります。


```xml
<package>
    <name>elec_parts</name>
</package>
```

# component file

# part component file

部品コンポーネントの場合はルート要素はpartです。

* name要素では、コンポーネント名を記載します。
* stl_fileでは部品の形状を表すstlファイルを指定します。対象のコンポーネントが属するpackageのディレクトリからの相対パスで入力します
* price/distribution/description ファイルの購入情報やメモを入れます。

```xml
<part>
    <name>pan_10</name>
    <stl_file>pan_10/m3_nabe_10.stl</stl_file>
    <price>3.5</price>
    <distributor>https://www.monotaro.com/p/3814/6604/</distributor>
    <description>sems screw is recommended</description>
</part>
```

# assemble component file
アセンブリコンポーネントでは親要素はassemblyです。
子要素のnameではコンポーネント名を指定します。
step要素は1つの組み立て手順を表します。1つのstepでは複数の部品を取り付けることが出来ます。

## 構成部品子要素
stepの子要素のcomponentでは取り付ける部品を指定します。pkg属性ではそのコンポーネントの属するパッケージ名を、type要素ではそのコンポーネント名を記載します。
origin要素では取付位置を記載します。単位はmmとdegです。
move要素では取りつける方向と長さを記載します。これは後々生成する組み立てgifに使用されます。真下方向の10mmの位置からから取り付ける場合はxyz="0 0 -10"と記載します。



## 視点子要素
<view>子要素では取付gifの視点を指定します。複数の<view>要素を記載することで、1つの取付stepについて複数の視点からのgifを生成します。
```xml
<?xml version="1.0" encoding="UTF-8"?>
<assembly>
    <name>side_asm</name>

    <step>
        <view from="70 20 30" to="0 0 0" angle="30" />
        <component pkg="sample_project" type="bar_plate">
            <origin xyz="0 0 0" rpy="0 0 90"/>
            <move xyz="0 0 0"/>
        </component>
    </step>
    <step>
        <view from="70 20 30" to="0 0 0" angle="30" />
        <view from="70 20 -30" to="0 0 0" angle="30" />
        <component pkg="screw_m3" type="pan_10">
            <origin xyz="10 0 4" rpy="0 0 0"/>
            <move xyz="0 0 15"/>
        </component>
        <component pkg="screw_m3" type="pan_10">
            <origin xyz="-10 0 4" rpy="0 0 0"/>
            <move xyz="0 0 15"/>
        </component>
        <component pkg="screw_m3" type="hollow_spacer_20">
            <origin xyz="10 0 -20" rpy="0 0 0"/>
            <move xyz="0 0 -10"/>
        </component>
        <component pkg="screw_m3" type="hollow_spacer_20">
            <origin xyz="-10 0 -20" rpy="0 0 0"/>
            <move xyz="0 0 -10"/>
        </component>
    </step>
</assembly>
```