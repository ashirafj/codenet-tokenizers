# C: tokenize <filepath> -l C -m json
# C++: tokenize <filepath> -l C++ -m json
# Java: tokenize <filepath> -l Java -m json
# Python: pytokenize <filepath> -m json -l

import json
import subprocess
import os
from . import Language

from typing import List, Dict


bin_path = os.path.join(os.path.dirname(__file__), "bin")
tokenizer_path = os.path.join(bin_path, "tokenize")
pytokenizer_path = os.path.join(bin_path, "pytokenize")

# change the tokenizers' execution permission
subprocess.run(["chmod", "+x", tokenizer_path])
subprocess.run(["chmod", "+x", pytokenizer_path])



class TokenizerBase:
    def __init__(self, language: Language):
        self.language = language

    def _get_tokenizer_cmd(self) -> List[str]:
        if (self.language is Language.Python):
            cmd = [ pytokenizer_path, "-m", "json", "-l" ]
        else:
            cmd = [ tokenizer_path, "-l", self.language.value, "-m", "json" ]
        return cmd

    def _decode_result(self, proc: subprocess.CompletedProcess) -> List[Dict[str, str]]:
        try:
            if (proc.stderr != None):
                err = proc.stderr.decode("utf8").strip()
                if (len(err) > 0):
                    return []
            return json.loads(proc.stdout.decode("utf8"))
        except json.decoder.JSONDecodeError:
            return []

    # トークナイザを実行してトークン一覧を取得
    def tokenize_from_file(self, filepath: str) -> List[Dict[str, str]]:
        cmd = self._get_tokenizer_cmd()
        cmd.append(filepath)
        proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        return self._decode_result(proc)

    # トークナイザを実行してトークン一覧を取得
    def tokenize(self, code: str) -> List[Dict[str, str]]:
        cmd = self._get_tokenizer_cmd()
        proc = subprocess.run(cmd, input = code.encode("utf8"), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        return self._decode_result(proc)


class Tokenizer(TokenizerBase):
    NEWLINE = "\n"

    def __init__(self, language: Language):
        super().__init__(language)

    # 1行分のトークン一覧をコードに整形
    def _format_line(self, tokens: List[Dict[str, str]]) -> str:
        code = ""
        current_position = 0
        for i, token in enumerate(tokens):
            raw = token["token"]
            column = int(token["column"])
            if (i == 0):
                code += raw
            else:
                if current_position < column:
                    # 空白が1つ以上で連結されていたトークンは空白1つで連結（空白2つが必要なものはない）
                    code += " " + raw
                else:
                    # 空白がなく連結されていたトークンはそのまま連結
                    code += raw
            current_position = column + len(raw)
        code += Tokenizer.NEWLINE
        return code

    # トークン一覧からコードに戻す
    def detokenize(self, tokens: List[Dict[str, str]]) -> str:
        # TODO: 空行無視を追加
        code = ""
        current_line = 1
        current_line_tokens = []
        for token in tokens:
            line = int(token["line"])
            
            # 行が変わったら出力
            if (current_line != line):
                code += self._format_line(current_line_tokens)
                current_line_tokens = []
                current_line = line

            current_line_tokens.append(token)
        
        # 最後に append されないので
        if (len(current_line_tokens) > 0):
            code += self._format_line(current_line_tokens)

        return code
