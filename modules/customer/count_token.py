import tiktoken
# enc = tiktoken.get_encoding("cl100k_base")


# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")
result = enc.encode("你好，有什么可以帮助你的吗？")
print(len(result))
enc2 = tiktoken.encoding_for_model("gpt-3.5-turbo")
result = enc2.encode("你好，有什么可以帮助你的吗？")
print(len(result))
pass
