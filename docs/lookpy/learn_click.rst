click模块简介
++++++++++++++

python快速创建命令行的一个第三方模块

安装
------
::

   pip install click


使用简单
---------
::

   # file: learn_click_demo.py
   import click
   @click.command()
   @click.option('--name', help="The name")

   def learn_click(name):
       """a example for use click module"""
       click.echo("The name is {}".format(ma,e))

   if __name__ == '__main__':
       learn_click()

然后在命令行可以查看帮助
::

　　python learn_click_demo.py --help

使用
::

　　python learn_click_demo.py --name wally

