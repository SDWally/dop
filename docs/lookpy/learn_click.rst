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

Value Options
~~~~~~~~~~~~~~~

::

    # Set a default value
    @click.command()
    @click.option('--n', default=1)
    def dots(n):
        click.echo('.' * n)

::

    # Show the default
    @click.command()
    @click.option('--n', default=1, show_default=True)
    def dots(n):
        click.echo('.' * n)


::

    # Make an option required
    @click.command()
    @click.option('--n', required=True, type=int)
    def dots(n):
        click.echo('.' * n)

::

    # More than one argument
    @click.command()
    @click.option('--pos', nargs=2, type=float)
    def findme(pos):
        click.echo('%s / %s' % pos)

::

    #　Tuples as Multi Value Options
    @click.command()
    @click.option('--item', type=(str, int))
    def putitem(item):
        click.echo('name=%s id=%d' % item)

::

    #　Tuples as Multi Value Options in another way
    @click.command()
    @click.option('--item', nargs=2, type=click.Tuple([str, int]))
    def putitem(item):
        click.echo('name=%s id=%d' % item)

::

    # Multiple Options
    @click.command()
    @click.option('--message', '-m', multiple=True)
    def commit(message):
        click.echo('\n'.join(message))


    $ commit -m foo -m bar
    foo
    bar

::

    # Counting
    @click.command()
    @click.option('-v', '--verbose', count=True)
    def log(verbose):
        click.echo('Verbosity: %s' % verbose)
    And on the command line:

    $ log -vvv
    Verbosity: 3

::

    # Boolean Flags
    import sys

    @click.command()
    @click.option('--shout/--no-shout', default=False)
    def info(shout):
        rv = sys.platform
        if shout:
            rv = rv.upper() + '!!!!111'
        click.echo(rv)

    $ info --shout
    LINUX!!!!111
    $ info --no-shout
    linux


More Options
--------------

::

    # Feature Switches
    import sys

    @click.command()
    @click.option('--upper', 'transformation', flag_value='upper',
                  default=True)
    @click.option('--lower', 'transformation', flag_value='lower')
    def info(transformation):
        click.echo(getattr(sys.platform, transformation)())

    $ info --upper
    LINUX
    $ info --lower
    linux
    $ info
    LINUX

::

    # Choice Options
    @click.command()
    @click.option('--hash-type', type=click.Choice(['md5', 'sha1']))
    def digest(hash_type):
        click.echo(hash_type)

    $ digest --hash-type=md5
    md5

    $ digest --hash-type=foo
    Usage: digest [OPTIONS]
    Try "digest --help" for help.

    Error: Invalid value for "--hash-type": invalid choice: foo. (choose from md5, sha1)

    $ digest --help
    Usage: digest [OPTIONS]

    Options:
      --hash-type [md5|sha1]
      --help                  Show this message and exit.

::

    # Password Prompts
    @click.command()
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True)
    def encrypt(password):
        click.echo('Encrypting password to %s' % password.encode('rot13'))

::

    # Password Prompts in another way
    @click.command()
    @click.password_option()
    def encrypt(password):
        click.echo('Encrypting password to %s' % password.encode('rot13'))

::

    # Dynamic Defaults for Prompts
    @click.command()
    @click.option('--username', prompt=True,
                  default=lambda: os.environ.get('USER', ''),
                  show_default='current user')
    def hello(username):
        print("Hello,", username)

::

    # Callbacks and Eager Options
    def print_version(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        click.echo('Version 1.0')
        ctx.exit()

    @click.command()
    @click.option('--version', is_flag=True, callback=print_version,
                  expose_value=False, is_eager=True)
    def hello():
        click.echo('Hello World!')

    $ hello
    Hello World!
    $ hello --version
    Version 1.0

::

    # Yes Parameters
    def abort_if_false(ctx, param, value):
        if not value:
            ctx.abort()

    @click.command()
    @click.option('--yes', is_flag=True, callback=abort_if_false,
                  expose_value=False,
                  prompt='Are you sure you want to drop the db?')
    def dropdb():
        click.echo('Dropped all tables!')

    $ dropdb
    Are you sure you want to drop the db? [y/N]: n
    Aborted!
    $ dropdb --yes
    Dropped all tables!


For more information about these changes see: https://click.palletsprojects.com/en/7.x/