# pre-commit plugin for the Microsoft Intelligent Data Platform

[pre-commit](https://pre-commit.com/) is a framework to develop hooks for [git](https://git-scm.com/).

Working with the [Microsoft Intelligent Data Platform](https://www.microsoft.com/en-us/microsoft-cloud/solutions/intelligent-data-platform) and is not optimal for git support.
Several files are always appended to at the end and thus will always lead to conflicts as soon as multiple developers work on feature branches in parallel.

The toolset in this repository helps to reduce the challenge significantly. It has the following features

- SSDT database projects
  - sort the sqlproj referennces to sql files
- SSIS integration services projects
  - sort the dtproj file where it lists the referenced dtsx files and where the parameters are cached
- Model.bim file sort
  - We create files in the same order as [Tabular Editor](https://github.com/TabularEditor/TabularEditor) to have a deterministic sort

# support
- reach ot to me
- reach out to me and my colleagues at [noventum](https://www.noventum.de/de/data-analytics/index.html ) to get a data warehouse incorporating this and many more best practices