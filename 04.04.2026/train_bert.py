import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd
from sklearn.model_selection import train_test_split

MODEL_NAME = "DeepPavlov/rubert-base-cased"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Загружаем данные
df = pd.read_csv("dataset.csv", encoding="utf-8")

label2id = {label: idx for idx, label in enumerate(df.intent.unique())}
id2label = {v: k for k, v in label2id.items()}

df["label"] = df.intent.map(label2id)

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df.text.tolist(),
    df.label.tolist(),
    test_size=0.2
)

def tokenize(texts):
    return tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

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

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label2id)
)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=4,
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

trainer.train()

model.save_pretrained("intent_model")
tokenizer.save_pretrained("intent_model")

print("Модель сохранена в папку intent_model")