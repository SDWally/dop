click模块简介
++++++++++++++

python快速创建命令行的一个第三方模块

安装
------
::

   pip install click


使用示例
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

在命令行查看帮助

::

 　　python learn_click_demo.py --help

使用

::

　 　python learn_click_demo.py --name wally

Command
----------

Creating a Command
~~~~~~~~~~~~~~~~~~~~~
::

    import click

    @click.command()
    def hello():
        click.echo('Hello World!')


Nesting Command
~~~~~~~~~~~~~~~~~
::

    @click.group()
    def cli():
        pass

    @click.command()
    def initdb():
        click.echo('Initialized the database')

    @click.command()
    def dropdb():
        click.echo('Dropped the database')

    cli.add_command(initdb)
    cli.add_command(dropdb)

Parameters
-----------

add parameters
~~~~~~~~~~~~~~~~~
::

    @click.command()
    @click.option('--count', default=1, help='number of greetings')
    @click.argument('name')
    def hello(count, name):
        for x in range(count):
            click.echo('Hello %s!' % name)

parameters type
~~~~~~~~~~~~~~~~~

- str
- int
- float
- bool
- click.UUID
- click.File
- click.Path
- click.Choice
- click.IntRange
- click.FloatRange
- click.DateTime

parameters name
~~~~~~~~~~~~~~~~
- For an option with ('-f', '--foo-bar'), the parameter name is foo_bar.

- For an option with ('-x',), the parameter is x.

- For an option with ('-f', '--filename', 'dest'), the parameter name is dest.

- For an option with ('--CamelCaseOption',), the parameter is camelcaseoption.

- For an arguments with (`foogle`), the parameter name is foogle.

Options
---------

Name Options
~~~~~~~~~~~~~~

Example A
::

    @click.command()
    @click.option('-s', '--string-to-echo')
    def echo(string_to_echo):
        click.echo(string_to_echo)

Example B
::

    @click.command()
    @click.option('-s', '--string-to-echo', 'string')
    def echo(string):
        click.echo(string)