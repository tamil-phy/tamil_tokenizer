"""
Example: Using TamilHFTokenizer for fine-tuning instead of BPE.

This script demonstrates how to:
1. Build a vocabulary from your Tamil corpus
2. Save/load the tokenizer
3. Use it with HuggingFace Transformers for fine-tuning

Prerequisites:
    pip install transformers torch datasets
"""

from tamil_tokenizer import TamilHFTokenizer


def build_and_save_tokenizer():
    """Step 1: Build vocabulary from your Tamil training data."""

    # Sample Tamil corpus — replace with your actual training data
    tamil_texts = [
        "அவன் வந்தான்.",
        "அவள் பள்ளிக்கு சென்றாள்.",
        "நான் தமிழ் படிக்கிறேன்.",
        "இந்தியா ஒரு பெரிய நாடு.",
        "தமிழ்நாடு அழகான மாநிலம்.",
        "மாணவர்கள் கல்வி கற்கின்றனர்.",
        "அவர்கள் வீட்டிற்கு திரும்பினார்கள்.",
        "இந்த புத்தகம் மிகவும் நல்லது.",
    ]

    # You can also pass a file path:
    # tamil_texts = "path/to/your/tamil_corpus.txt"  # one sentence per line

    # Create tokenizer — choose your level:
    #   "morpheme" — best BPE replacement (root + suffixes)
    #   "word"     — word-level tokens
    #   "character" — Tamil letter-level tokens
    tokenizer = TamilHFTokenizer(level="morpheme")

    # Build vocabulary (set min_frequency to filter rare tokens)
    vocab_size = tokenizer.build_vocab(tamil_texts, min_frequency=1)
    print(f"Vocabulary size: {vocab_size}")

    # Save for later use
    tokenizer.save_pretrained("./tamil_morpheme_tokenizer")
    print("Tokenizer saved to ./tamil_morpheme_tokenizer")

    return tokenizer


def load_and_encode():
    """Step 2: Load tokenizer and encode text."""

    tokenizer = TamilHFTokenizer.from_pretrained("./tamil_morpheme_tokenizer")
    print(f"Loaded tokenizer: {tokenizer}")

    text = "அவன் பள்ளிக்கு சென்றான்."
    # Encode
    encoded = tokenizer(text, return_tensors="pt", padding=True)
    print(f"\nText: {text}")
    print(f"Token IDs: {encoded['input_ids']}")
    print(f"Attention mask: {encoded['attention_mask']}")

    # Decode back
    decoded = tokenizer.decode(encoded["input_ids"][0], skip_special_tokens=True)
    print(f"Decoded: {decoded}")

    # See individual tokens
    tokens = tokenizer.tokenize(text)
    print(f"Tokens: {tokens}")


def finetune_example():
    """
    Step 3: Use with HuggingFace Trainer for fine-tuning.

    This is a skeleton — adapt model name and dataset to your use case.
    """
    try:
        from transformers import (
            AutoModelForCausalLM,
            TrainingArguments,
            Trainer,
            DataCollatorForLanguageModeling,
        )
        from datasets import Dataset
    except ImportError:
        print("Install: pip install transformers torch datasets")
        return

    tokenizer = TamilHFTokenizer.from_pretrained("./tamil_morpheme_tokenizer")

    # --- Prepare dataset ---
    tamil_texts = [
        "தமிழ் ஒரு பழமையான மொழி.",
        "சென்னை தமிழ்நாட்டின் தலைநகரம்.",
        "கல்வி அறிவை வளர்க்கும்.",
    ]

    def tokenize_fn(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=128,
            padding="max_length",
        )

    dataset = Dataset.from_dict({"text": tamil_texts})
    tokenized_dataset = dataset.map(tokenize_fn, batched=True, remove_columns=["text"])

    print(f"Dataset size: {len(tokenized_dataset)}")
    print(f"Sample: {tokenized_dataset[0]}")

    # --- Fine-tune (skeleton) ---
    # Replace "gpt2" with your base model
    # model = AutoModelForCausalLM.from_pretrained("gpt2")
    # model.resize_token_embeddings(len(tokenizer))
    #
    # training_args = TrainingArguments(
    #     output_dir="./tamil_finetuned",
    #     num_train_epochs=3,
    #     per_device_train_batch_size=4,
    #     learning_rate=5e-5,
    #     save_steps=500,
    # )
    #
    # data_collator = DataCollatorForLanguageModeling(
    #     tokenizer=tokenizer, mlm=False
    # )
    #
    # trainer = Trainer(
    #     model=model,
    #     args=training_args,
    #     train_dataset=tokenized_dataset,
    #     data_collator=data_collator,
    # )
    #
    # trainer.train()

    print("\nTokenizer is ready for fine-tuning!")
    print("Uncomment the model/trainer code above and adapt to your model.")


if __name__ == "__main__":
    print("=" * 60)
    print("Step 1: Build & save tokenizer")
    print("=" * 60)
    build_and_save_tokenizer()

    print("\n" + "=" * 60)
    print("Step 2: Load & encode")
    print("=" * 60)
    load_and_encode()

    print("\n" + "=" * 60)
    print("Step 3: Fine-tuning skeleton")
    print("=" * 60)
    finetune_example()
