#### 1. 安装
##### (1). 方法1：使用pip安装
~~~
pip install icare-nlp
Pypi链接: https://pypi.org/project/icare-nlp/
~~~
##### (2). 方法2： 使用Source Codes安装
~~~
git clone https://github.com/YiyiyiZhao/icare_nlp_tools.git
cd icare_nlp_tools
pip install -e .
pip install -r rewuirements.txt
~~~

#### 2. 使用
##### 2.0 Task_Disp: 输入User query, 输出对应下列四种的Task类型
###### (1). Commands
###### (2). Demo

##### 2.1 Object_Desc: 输入object detection list, 输出场景播报
###### (1). Commands
###### (2). Demo

##### 2.2 Object_QA: 输入object detection list 和 Question, 输出场景有关的Answer
###### (1). Commands
###### (2). Demo

##### 2.3 Receipt_Desc: 输入Receipt的OCR识别文本, 输出Receipt描述
###### (1). Commands
###### (2). Demo

##### 2.4 Receipt_QA: 输入Receipt的OCR识别文本, 输出票据总价
###### (1). Commands
###### (2). Demo

#### Run Example
~~~
from icare_nlp.object_qa import ObjectQA
#question
#obj_detect
ans=object_qa.form_response(question, obj_detect)
~~~
~~~
cd  examples
python object_qa.py > qa.out
可以查看qa.out文件查看输入object_detect 和 question下，输出的answer
~~~