from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset

print("Loading dataset...")
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")
print(f"Loaded {len(dataset)} examples")

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

print("Formatting data...")
def fmt(ex):
    texts = [f"Question: {i}Answer: {r}{tokenizer.eos_token}" for i,r in zip(ex["instruction"], ex["response"])]
    return tokenizer(texts, truncation=True, max_length=256)

dataset = dataset.map(fmt, batched=True, remove_columns=dataset.column_names)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

print("Starting training...")
trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./military_ai_model",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_steps=5000,
        logging_steps=500,
        save_total_limit=2,
        report_to="none",
    ),
    train_dataset=dataset,
    data_collator=data_collator,
)

trainer.train()
trainer.save_model("./military_ai_model")
tokenizer.save_pretrained("./military_ai_model")
print("Training complete! Model saved to ./military_ai_model")
