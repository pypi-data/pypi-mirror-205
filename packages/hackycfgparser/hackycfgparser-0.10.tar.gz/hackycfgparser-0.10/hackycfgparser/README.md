# Hacky config parser - parses ConfigParser-compatible files / sys.argv and changes the defaults of functions

### pip install hackycfgparser

#### Tested against Windows 10 / Python 3.10 / Anaconda


The goal of this project is to create a decorator function that can modify the default arguments of a given function using values passed through both ConfigParser-compatible files and command line arguments. To achieve this, we first check if the input function is callable or None. Then, we retrieve the global dictionary of the calling frame and define a decorator function.

The decorator function works by modifying the default arguments of the input function based on the values passed through the command line arguments. To do this, we first retrieve the variable names and annotations of the input function and create a dictionary of all the annotations. We then iterate through the default arguments of the input function and attempt to convert them to the appropriate data type based on the annotations. If the conversion fails, we try all possible data types until a successful conversion is made.

Finally, the modified default arguments are set, and the input function is called with the modified arguments. This allows for greater flexibility and customization when working with functions, making it easier to pass in arguments from different sources without needing to modify the function nor the function calls themselves.

There is also a standalone version of the sys.argv parser: 
https://github.com/hansalemaos/hackyargparser

### How to use it

```python


from hackycfgparser import load_config_file_vars, add_config, config

load_config_file_vars(cfgfile=r"C:\testcfg.ini", onezeroasboolean=False)
config.helptext = (
    "Error! --f2_a, --f2_b, --f1_a are mandatory!"  # The help text to be printed
)
config.kill_when_not_there(
    ("--f2_a", "--f2_b", "--f1_a")
)  # If those arguments are not passed, config.helptext will be printed, and sys.exit will be called
config.stop_after_kill = True  # Stop after printing config.helptext -> input()


# example of a config file (put Iterables in double quotes"")
'''[book]
title: The Python Standard Library
author: Fredrik Lundh
email: fredrik@pythonware.com
version: 2.0-001115
pages: 250
f1_a: 14.5
f1_b: 22
f2_a: 1444.5
f2_b: 2244
f3_a: "(14446.5,20,33)"
f3_b: 2266
mvar:1099324
didi:"{2:3,5:6}"
dudu:"{2,3,5,6}"'''


@add_config
def function10(
    didi: dict | None = None,
    dudu: set | None = None,
    mvar: int = 10,
):
    print(didi, dudu)
    return didi, dudu, mvar


@add_config
def function1(
    f1_a: int | float | None = None,
    f1_b: int | float = 1,
    mvar: int = 10,
):
    print(f1_b * f1_a * mvar)
    return f1_a, f1_b, mvar


@add_config
def function2(
    f2_a: int | float | None = None,
    f2_b: int | float | None = None,
    mvar: int = 10,
):
    print(f2_a * f2_b * mvar)

    return f2_a, f2_b, mvar


@add_config
def function3(
    f3_a: list | tuple = (),
    f3_b: int | float = 1,
):
    for l in f3_a:
        print(l + f3_b)

    return set(f3_a)


def function4(
    f3_a: list | tuple = (),
    f3_b: int | float = 1,
):
    print("i am not decorated")
    print(f"{f3_a=}, {f3_b=}")

    return set(f3_a)


@add_config
def baba(title: str = "", email: str = "", pages: int = 0):
    print(title, email, pages)


@add_config
def baba2(title2: str = "", email2: str = "", pages2: int = 0):
    print(title2, email2, pages2)
    return title2 + email2


print(f"\n=========\n{function2()=}")
print(f"\n=========\n{function1()=}")
print(f"\n=========\n{function3()=}")
print(f"\n=========\n{function4()=}")
print(f"\n=========\n{baba()=}")
print(f"\n=========\n{function10()=}")
print(f"\n=========\n{baba2()=}")

#  (dfdir) PS C:\ProgramData\anaconda3\envs\dfdir> .\python.exe .\hackycfg.py --title2 bababadxd --email2 ooooooo pages2 555
# 3563412574392.0
#
# =========
# function2()=(1444.5, 2244, 1099324)
# 350684356.0
#
# =========
# function1()=(14.5, 22, 1099324)
# 16712.5
# 2286
# 2299
#
# =========
# function3()={33, 20, 14446.5}
# i am not decorated
# f3_a=(), f3_b=1
#
# =========
# function4()=set()
# 'The Python Standard Library' 'fredrik@pythonware.com' 250
#
# =========
# baba()=None
# {2: 3, 5: 6} {2, 3, 5, 6}
#
# =========
# function10()=({2: 3, 5: 6}, {2, 3, 5, 6}, 1099324)
# bababadxd ooooooo 0
#
# =========
# baba2()='bababadxdooooooo'



```