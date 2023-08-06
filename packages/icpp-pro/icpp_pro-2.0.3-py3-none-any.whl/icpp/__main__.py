"""__main__.py
The double underscores indicate that this file has a special meaning in Python.
When running a package (!) as a script with -m, 'python -m icpp', Python
executes the contents of the __main__.py file.

In other words, __main__.py acts as the entry point of our program and takes care of
the main flow, calling other parts as needed

reference: https://realpython.com/pypi-publish-python-package/
"""
count = 0
def main() -> None:
    """Entry point of program"""
    global count
    if count==0:
        print("")
        print("You installed the placeholder package `icpp-pro` from PyPI")
        print("Please contact us at icpp@icpp.world for installation & licensing instructions.")
        print("")
        count = count+1


#
# Always start it up or debug as a module:
#  python -m icpp.__main__
#
main()