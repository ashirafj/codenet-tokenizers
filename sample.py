from codenet_tokenizers.tokenizers import PyTokenizer

def read():
	with open("sample_target.py") as f:
		return f.read()

if __name__ == "__main__":
	tokenizer = PyTokenizer()
	code = read()
	normalized_code = tokenizer.normalize(code)
	normalized_tokens = tokenizer.normalize_separated(code)

	print("-" * 100)
	print(code)
	print("-" * 50)
	print(normalized_code)
	print("-" * 50)
	print(normalized_tokens)
	print("-" * 100)
