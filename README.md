#### 1. 安装
##### (1). 方法1：使用pip安装
~~~
pip install icare-nlp
Pypi链接: https://pypi.org/project/icare-nlp/
~~~
##### (2). 方法2： 使用Source Codes安装
~~~

~~~

#### 使用
~~~
from icare_nlp.object_qa import ObjectQA
#question
#obj_detect
ans=object_qa.form_response(question, obj_detect)
~~~

#### Run Example
~~~
cd  examples
python object_qa.py > qa.out
可以查看qa.out文件查看输入object_detect 和 question下，输出的answer
~~~