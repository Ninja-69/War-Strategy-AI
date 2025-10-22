from transformers import pipeline

print("Loading model...")
model = pipeline("text-generation", model="./military_ai_model")

question = "What was Napoleon's strategy at Waterloo?"
print("Question:", question)
print("Generating answer...")

response = model(question, max_length=200, num_return_sequences=1)
print("Answer:", response[0]['generated_text'])
