from ai.structured import analyze_product_question


result = analyze_product_question(
    "Why might users abandon an e-commerce checkout?"
)

print(result)
print(type(result))
print(result.question)
print(result.possible_reasons)