import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd
from sklearn.model_selection import train_test_split

print("1. Загрузка датасета...")
df = pd.read_csv("dataset.csv", encoding="utf-8")

labels = [
    "greeting",
    "goodbye",
    "time",
    "date",
    "year",
    "weather",
    "smalltalk",
    "help",
    "unknown"
]

label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {v: k for k, v in label2id.items()}
df["label"] = df.intent.map(label2id)

print(f"   Intents: {label2id}")
print(f"   Всего примеров: {len(df)}")

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df.text.tolist(),
    df.label.tolist(),
    test_size=0.2,
    random_state=42
)

print("2. Загрузка токенизатора...")
MODEL_NAME = "DeepPavlov/rubert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)

print("3. Токенизация...")
train_encodings = tokenize(train_texts)
val_encodings = tokenize(val_texts)

class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

print("4. Загрузка модели...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(label2id), id2label=id2label, label2id=label2id)

print("5. Настройка обучения...")
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=10,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",
    logging_dir="./logs",
    learning_rate=2e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

print("6. Запуск обучения...")
trainer.train()

print("7. Сохранение модели...")
model.save_pretrained("intent_model")
tokenizer.save_pretrained("intent_model")

print("Модель сохранена в папку intent_model")