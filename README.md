# Molingo

Mo(re)lingo is a *frontend component* that swiftly converts CSV and XLSX files into internationalization files. It does not implement specific internationalization capabilities but defers to excellent internationalization solutions on various platforms. For instance, in iOS, it is powered by SwiftGen, and in Flutter, it utilizes GetX. Molingo's main function is to transform CSV and XLSX files into the required frontend files for internationalization on different platforms (such as strings, JSON, etc.), much like a *frontend* in a build system. You can provide your own implementation by configuring plugins in the lingo.yml file.

# Installation

To get started with Molingo, follow these steps:

1. Download the project
2. Navigate to the project directory
3. Execute the `setup.sh` script:
   ```shell
   sh setup.sh
   ```
4. Configure your project path in lingo.yml
5. You can now run the `molingo` command from anywhere.

# Uninstallation

just run 

```shell
sh uninstall.sh
```
and remove molingo project.

# Requirements

Before using Molingo, please ensure you have the following dependencies installed:

1. Python 3
2. Homebrew
3. Flutter (for Flutter)