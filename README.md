# codenet-tokenizers

A wrapper library for tokenizers from CodeNet Project.

## Setup

Install the library from this repository.

```
pip install git+https://github.com/ashirafj/codenet-tokenizers
```

## Usage

### Initialize

For Python source code,
```py
from codenet_tokenizers.tokenizers import PyTokenizer
tokenizer = PyTokenizer()
```

For C source code,
```py
from codenet_tokenizers.tokenizers import CTokenizer
tokenizer = CTokenizer()
```

For C++ source code,
```py
from codenet_tokenizers.tokenizers import CppTokenizer
tokenizer = CppTokenizer()
```

For Java source code,
```py
from codenet_tokenizers.tokenizers import JavaTokenizer
tokenizer = JavaTokenizer()
```

### Tokenize

To tokenize the source code, separate by each line, and remove unnecessary tokens,
```py
normalized_tokens = tokenizer.normalize_separated(code)
```

### Normalize

To normalize the source code based on tokenized results,
```py
normalized_code = tokenizer.normalize(code)
```
