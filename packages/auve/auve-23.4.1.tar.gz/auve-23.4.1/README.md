# auve

auve is a very simple Python tool to provide auto-generated version texts that can be used as version numbers in any Python project.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install auve.

```bash
pip install auve
```

## Usage

In it's simplest form use it like so:

```python
from auve import AutoVersionNumber

# returns a version number like "22.8.0"
print(AutoVersionNumber().version)

# returns a build text like "22.308.1100"
print(AutoVersionNumber().build)

# returns a release text like "2022-08-11"
print(AutoVersionNumber().release)

# returns a full version number like
# "version: 22.8.0, build_22.308.1100, release 2022-08-11"
print(AutoVersionNumber().full_version)
```

'auve' comes from 'AUtomatic VEersionnumber' and therefor is an update method that will automatically update the version number - but this works with version files only, so it is also possible to store a version number in a file. Provide a file name and it will get created in the CWD.

```python
from auve import AutoVersionNumber

# there are no rules for the file name, something like '.version' or 'VERSION' seems fine
# this file will by default be created in the CWD
file = "DEMO_VERSION"
# relative paths are also possible
# if the provided path not exists it also gets created
file = "./foo/DEMO_VERSION"

# date: 2022-08-11
# day of year: 308
# time: 11:00
# if there is no file auve creates it
# returns something like: "22.8.0"
print(AutoVersionNumber(file))

# returns a build number like "22.308.1100", from file
print(AutoVersionNumber(file).build)

# returns a release number like "2022-08-11", from file
print(AutoVersionNumber(file).release)

# returns a full version number like
# "version: 22.8.0, build_22.308.1100, release 2022-08-11", from file
print(AutoVersionNumber(file).full_version)
```

The parts of the version text are simply generated from the actual date and time when using the tool.
The update method updates the version number depending on the month, eg. if it is August in 2022, the version number uses '22' and '08' as primary and secondary parts of the version number. When initializing a version for the first time, the third part (one could see this as 'micro' or 'patch' part) will be set to '0'. When updating this version number from a file, this 'micro' or 'patch' part will be increased by '1' - as long as the year is still '22' and the month is still '08' in this particular example. If not, these parts also will be updated to the actual year and month and 'micro'/'patch' will again be set to '0'.
The 'build' and 'release' strings also depend on the actual date and time, when doing the update.

```python
# date: 2022-08-15
# day of year: 312
# time: 16:30
# returns "True"
print(AutoVersionNumber(file).update())

# returns a full version number like
# "version: 22.8.1, build_22.312.1630, release 2022-08-15", from file
print(AutoVersionNumber(file).full_version)
```

## Demo

There is also a simple demo module in the package:

```python
from auve import demo

demo()
```

Please take note that when running this demo script a file named "DEMO_VERSION" will be generated in the CWD. This file is just for demonstration purposes and can be deleted after running the demo.

## License

[MIT](https://choosealicense.com/licenses/mit/)
