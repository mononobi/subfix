# Subfix

A simple subtitle encoding fixer.

Subfix is a utility package which helps to convert subtitle file encodings.

# Features

- Single File Conversion
- Batch Conversion

# Installing

**Install using pip**:

**`pip install subfix`**

# Example:

*Single:*
```python
from subfix.converter.manager import converter_manager


converter_manager.convert('/home/user/movies/system-crasher-2019/english_sub.srt')
```
*Batch:*
```python
from subfix.converter.manager import converter_manager


converter_manager.batch_convert('/home/user/movies/system-crasher-2019')
```
*Both methods accept extra optional inputs to customize the conversion.*
<br>
*Read the docstrings for more information on extra options.*