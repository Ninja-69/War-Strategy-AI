from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import torch

print("Loading dataset...")
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")
print(f"Loaded {len(dataset)} examples")

print("Loading GPT-2 XL model (1.5B parameters)...")
model_name = "gpt2-xl"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

print("Formatting data with proper Q&A structure...")
def format_data(examples):
    texts = []
    for inst, resp in zip(examples["instruction"], examples["response"]):
        text = f"### Question: {inst}### Answer: {resp}{tokenizer.eos_token}"
        texts.append(text)
    
    return tokenizer(
        texts,
        truncation=True,
        max_length=512,
        padding="max_length"
    )

dataset = dataset.map(
    format_data,
    batched=True,
    remove_columns=dataset.column_names,
    desc="Formatting data"
)

print("Starting ULTIMATE training (10 epochs, GPT-2 XL)...")
training_args = TrainingArguments(
    output_dir="./military_ai_ultimate",
    num_train_epochs=10,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=1e-5,
    warmup_steps=1000,
    logging_steps=50,
    save_steps=2500,
    save_total_limit=3,
    fp16=False,
    weight_decay=0.01,
    max_grad_norm=1.0,
    report_to="none",
    lr_scheduler_type="cosine"
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)

print("="*50)
print("TRAINING STARTED!")
print("Model: GPT-2 XL (1.5B parameters)")
print("Epochs: 10")
print("Estimated time: 96 hours (4 days)")
print("="*50)

trainer.train()

print("Training complete! Saving ultimate model...")
model.save_pretrained("./military_ai_ultimate")
tokenizer.save_pretrained("./military_ai_ultimate")
print("🎉 DONE! You now have a BEAST military AI!")
