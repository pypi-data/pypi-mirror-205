Install 
```shell
pip install aws_lambda_mess
```

Check install
```shell
alm --help
```

Start a project
```shell
alm new demo
```
This creats a new directory under the current directory.

Build the zip fiule to upload to aws
```shell
cd demo
alm build
```





----------------
Build aws_lambda_mess
```shell
hatch build
```
Upload to pip
```shell
py -m twine upload dist/* --user johanjordaan
```




