from . import Language
from .base_tokenizers import TokenizerBase, Tokenizer
from typing import List, Dict

class PyTokenizer(TokenizerBase):
    INDENT = " " * 4
    NEWLINE = "\n"

    def __init__(self):
        super().__init__(Language.Python)

    # 1行分のトークン一覧をコードに整形
    def _format_line(self, tokens: List[Dict[str, str]], indent_count: int) -> List[str]:
        LITERALS = [ "integer", "floating", "string", "character" ]
        tokens_line = [PyTokenizer.INDENT] * indent_count
        literal_count = 0
        for i, token in enumerate(tokens):
            cls = token["class"]
            raw = token["token"]
            # リテラル
            if (cls in LITERALS):
                if literal_count == 0:
                    tokens_line.append(" ")
                tokens_line.append(str(raw))
                literal_count += 1
            else:
                if i > 0:
                    tokens_line.append(" ")
                tokens_line.append(str(raw))
                literal_count = 0
        return tokens_line

    # トークン一覧からコードに戻す
    def _detokenize(self, tokens: List[Dict[str, str]], ignore_whiteline: bool = True) -> List[List[str]]:
        tokens_lines = []
        current_line_tokens = []
        indent_count = 0
        for token in tokens:
            cls = token["class"]
            raw = token["token"]

            if (cls == "layout" and raw == "INDENT"):
                indent_count += 1
            elif (cls == "layout" and raw == "DEDENT"):
                indent_count -= 1
            elif (cls == "layout" and raw == "NEWLINE"):
                # 空行かつ空行無視時はスキップ
                if len(current_line_tokens) == 0 and ignore_whiteline:
                    continue

                # 1行分の溜めたトークン一覧を整形
                tokens_lines.append(self._format_line(current_line_tokens, indent_count))
                current_line_tokens = []
            else:
                current_line_tokens.append(token)
        
        # 最後に改行がないとき append されないので
        if (len(current_line_tokens) > 0):
            tokens_lines.append(self._format_line(current_line_tokens, indent_count))
        return tokens_lines

    # コメントや空行を除去したコードを取得（識別子は維持）
    def normalize(self, raw_code: str, ignore_whiteline: bool = True) -> str:
        tokens = super().tokenize(raw_code)
        tokens_lines = self._detokenize(tokens, ignore_whiteline)

        normalized_code = ""
        for tokens_line in tokens_lines:
            line = "".join(tokens_line) + PyTokenizer.NEWLINE
            normalized_code += line

        return normalized_code

    # コメント等を除去した行ごとのコードを取得（識別子は維持）
    def normalize_separated(self, raw_code: str, ignore_whiteline: bool = True) -> List[List[str]]:
        tokens = super().tokenize(raw_code)
        tokens_lines = self._detokenize(tokens, ignore_whiteline)
        return tokens_lines



class CTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(Language.C)

    # コメントや空行を除去したコードを取得（識別子は維持）
    def normalize(self, raw_code: str) -> str:
        tokens = super().tokenize(raw_code)
        normalized_code = super().detokenize(tokens)
        return normalized_code


class CppTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(Language.CPP)

    # コメントや空行を除去したコードを取得（識別子は維持）
    def normalize(self, raw_code: str) -> str:
        tokens = super().tokenize(raw_code)
        normalized_code = super().detokenize(tokens)
        return normalized_code


class JavaTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(Language.Java)

    # コメントや空行を除去したコードを取得（識別子は維持）
    def normalize(self, raw_code: str) -> str:
        tokens = super().tokenize(raw_code)
        normalized_code = super().detokenize(tokens)
        return normalized_code
