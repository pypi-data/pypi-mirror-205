import re
import time
import datetime
import math

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import pandas as pd

from tqdm.auto import tqdm
from torch.utils.data import DataLoader, Dataset
from utils.KoCharELECTRA.tokenization_kocharelectra import KoCharElectraTokenizer
from model.LSTM_model import Seq2SeqModel

tokenizer = KoCharElectraTokenizer.from_pretrained("monologg/kocharelectra-base-discriminator")

special_tokens_dict = {'additional_special_tokens': ['<N>', '</N>']}
tokenizer.add_special_tokens(special_tokens_dict)
print(tokenizer.all_special_tokens)
print(tokenizer.all_special_ids)

# 11568, 11569
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class TargetDataset(Dataset):
    def __init__(self, trg_path, max_len):
        super(TargetDataset, self).__init__()
        self.target = []
        self.max_len = max_len

        with open(trg_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = eval(line)
                self.target.append(line)


    def __len__(self):
        return len(self.target)

    def __getitem__(self, idx):
        return self.target[idx]

class TranslationDataset(Dataset):
    def __init__(self, src_path, max_len):
        super(TranslationDataset, self).__init__()
        self.src_sents = []
        self.tgt_sents = []
        self.pairs = []
        self.max_len = max_len

        print(src_path)

        with open(src_path, 'r', encoding='utf-8') as f:
            for line in f:
                pair = line.strip().split("\t")
                if len(pair) == 2:
                    src_sent, tgt_sent = pair
                    self.pairs.append((src_sent, tgt_sent))

                else:
                    print("[pair error]", pair)

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        src_sent, tgt_sent = self.pairs[idx]

        # 소스 문장 전처리
        src_sent = src_sent.lower()
        src_ids = tokenizer.encode(src_sent, add_special_tokens=True, max_length=self.max_len, padding='max_length', truncation=True)
        src_tensor = torch.tensor(src_ids)

        # 타겟 문장 전처리
        tgt_sent = tgt_sent.lower()
        tgt_sent = tgt_sent.replace("[", "<N>").replace("]", '</N>')
        tgt_ids = tokenizer.encode(tgt_sent, add_special_tokens=True, max_length=self.max_len, padding='max_length', truncation=True)
        tgt_tensor = torch.tensor(tgt_ids)

        return src_tensor, tgt_tensor

def train(model, train_data, val_data, val_y, optimizer, criterion, device, epochs, clip, patience, batch_size, save_path):
    best_loss = float('inf')
    train_losses, val_losses = [], []
    early_stop_count = 0

    for epoch in range(epochs):
        model.train()
        train_loss = 0
        train_acc = 0

        epoch_iterator = tqdm(train_data, desc=f"Training epoch {epoch+1}/{epochs} loss=X.X", dynamic_ncols=True)
        for index, batch in enumerate(epoch_iterator):
            src_batch, trg_batch = batch

            # encode and decode the batch
            src_tensor = src_batch.to(device)
            trg_tensor = trg_batch.to(device)

            optimizer.zero_grad()


            output = model(src_tensor, trg_tensor)
            # output: [출력 단어 개수, 배치 크기, 출력 차원]
            output_dim = output.shape[-1]

            # reshape for loss calculation
            output = output.view(-1, output_dim)
            trg_tensor = trg_tensor.view(-1)

            loss = criterion(output, trg_tensor)

            preds = torch.argmax(output, dim=-1)

            # backpropagation
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
            optimizer.step()

            train_loss += loss.item()

            epoch_iterator.set_description(f"Training epoch {epoch+1}/{epochs} loss={loss} PPL={math.exp(loss)}")

        train_loss /= len(train_data)
        train_losses.append(train_loss)

        # evaluate on validation set
        val_loss = evaluate(model, val_data, val_y, criterion,batch_size, device)
        val_losses.append(val_loss)

        print(f"Epoch: {epoch+1}, Train Loss: {train_loss:.4f}, Train PPL: {math.exp(train_loss)}|"
              f" Val Loss: {val_loss:.4f}, Val PPL:{math.exp(val_loss)}")

        # early stopping
        if val_loss < best_loss:
            early_stop_count = 0
            best_loss = val_loss
            torch.save(model.state_dict(), f"{save_path}/LSTM_postprocessing_best_model.pt")
        else:
            early_stop_count += 1
            print("early_stop_count:", early_stop_count)
            if early_stop_count >= patience:
                print(f"Validation loss didn't improve for {patience} epochs. Training stopped.")
                break

    return train_losses, val_losses


def evaluate(model, dataloader, val_y, criterion, batch_size, device):
    """Evaluate the model on validation/test dataset"""
    model.eval()
    total_loss = 0.
    total_correct = 0
    total = len(dataloader) * batch_size

    pbar = tqdm(dataloader, desc="Validation")
    with torch.no_grad():
        for index, batch in enumerate(pbar):
            src, trg = batch
            src = src.to(device)
            trg = trg.to(device)

            trg_word = val_y[index * batch_size: (index + 1) * batch_size]

            output = model(src, trg, 0)  # ignore <eos> token

            # acc
            for i in range(trg.shape[0]):
                # 412 = [, 413 = ]

                preds = torch.argmax(output[i], dim=-1).cpu().numpy()
                target = trg[i].cpu().numpy()
                source = tokenizer.decode(src[i], skip_special_tokens=True)
                true = trg[i].cpu().numpy()
                true = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in true],
                                         skip_special_tokens=True)
                pred = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in preds],
                                         skip_special_tokens=True)

                if pred == true:
                    # total_correct += len(trg_word[i])
                    total_correct += 1
                    continue

                else:
                    target_word = re.findall('\[(.*?)\]', pred)
                    if len(target_word) == len(trg_word[i]):
                        for j in range(len(trg_word[i])):
                            if target_word[j] == trg_word[i][j]:
                                is_equal = True
                            else:
                                is_equal = False

                    else:
                        continue

                    if is_equal:
                        total_correct += 1


            output_dim = output.shape[-1]
            output = output[1:].view(-1, output_dim)
            trg = trg[1:].view(-1)
            loss = criterion(output, trg)
            total_loss += loss.item()


            pbar.set_description(f"ACC {total_correct}/{total} = {total_correct/total},"
                                      f"LOSS = {loss:.4f}")

    avg_loss = total_loss / len(dataloader)

    return avg_loss

def init_weights(m):
    for name, param in m.named_parameters():
        nn.init.uniform_(param.data, -0.08, 0.08)

def translate_sentence(dataloader, test_y, batch_size, model, device, max_len):
    model.eval()
    total = len(dataloader) * batch_size
    total_correct = 0
    is_equal = False
    df_wrong = pd.DataFrame(columns=['Source', 'Target', 'Prediction'])
    df_correct = pd.DataFrame(columns=['Source', 'Target', 'Prediction'])

    with torch.no_grad():
        for index, batch in enumerate(dataloader):
            src, trg = batch
            src = src.to(device)
            trg = trg.to(device)

            trg_word = test_y[index * batch_size : (index+1) * batch_size]

            output = model(src, trg, 0)  # ignore <eos> token

            try:

                for i in range(batch_size):
                    # 412 = [, 413 = ]

                    preds = torch.argmax(output[i], dim=-1).cpu().numpy()
                    source = tokenizer.decode(src[i], skip_special_tokens=True)
                    true = trg[i].cpu().numpy()
                    true = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in true],
                                             skip_special_tokens=True)
                    pred = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in preds],
                                             skip_special_tokens=True)

                    if pred == true:
                        total_correct += 1
                        # total_correct += len(trg[i])
                        df_correct = df_correct.append({"Source": source, "Target": true, "Prediction": pred},
                                                       ignore_index=True)
                        continue

                    else:
                        target_word = re.findall('\[(.*?)\]', pred)
                        if len(target_word) == len(trg_word[i]):
                            for j in range(len(trg_word[i])):
                                if target_word[j] == trg_word[i][j]:
                                    is_equal = True
                                else:
                                    is_equal = False

                        else:
                            df_wrong = df_wrong.append({"Source": source, "Target": true, "Prediction": pred},
                                                       ignore_index=True)
                            continue

                        if is_equal:
                            total_correct += 1
                            df_correct = df_correct.append({"Source": source, "Target": true, "Prediction": pred},
                                                           ignore_index=True)
                        else:
                            df_wrong = df_wrong.append({"Source": source, "Target": true, "Prediction": pred},
                                                       ignore_index=True)
            except:
                pass

    print(total, total_correct)
    print("ACC: ", total_correct/total)

    # 결과 저장
    df_correct.to_csv("./results/correct_cell.csv", index=False, encoding='utf-8-sig')
    df_wrong.to_csv("./results/wrong_cell.csv", index=False, encoding='utf-8-sig')

def inference(data, batch_size, model):
    start = time.time()
    model.eval()
    output_list = []
    with torch.no_grad():
        for index, batch in enumerate(data):
            src, trg = batch
            src = src.to(device)
            trg = trg.to(device)

            output = model(src, trg, 0)  # ignore <eos> token

            for i in range(trg.shape[0]):
                # 412 = [, 413 = ]
                preds = torch.argmax(output[i], dim=-1).cpu().numpy()
                pred = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in preds],
                                         skip_special_tokens=True)

                output_list.append(pred)
    end = time.time()
    sec = (end - start)
    result = datetime.timedelta(seconds=sec)
    print("time:", result)
    print(len(data))
    return output_list

def main():
    print(device)
    # 하이퍼파라미터 설정
    hidden_size = 512 # 512
    embed_size = 256 #
    dropout = 0.3
    num_layers = 2
    batch_size = 64
    learning_rate = 0.0001
    num_epochs = 100
    patience = 3
    max_len = 128

    # 데이터셋 생성
    train_data = TranslationDataset('data/special_window_train.txt', max_len)
    val_data = TranslationDataset('data/special_window_val.txt', max_len)
    test_data = TranslationDataset('data/special_window_test.txt', max_len)

    train_y = TargetDataset("data/special_window_train_target.txt", max_len)
    val_y = TargetDataset("data/special_window_val_target.txt", max_len)
    test_y = TargetDataset("data/special_window_test_target.txt", max_len)

    # 소스와 타겟의 vocab 크기 설정
    src_vocab_size = len(tokenizer.get_vocab())
    tgt_vocab_size = len(tokenizer.get_vocab())

    # 모델 생성
    model = Seq2SeqModel(src_vocab_size, tgt_vocab_size, embed_size, hidden_size, num_layers, dropout, device, tokenizer).to(device)
    model.apply(init_weights)

    # 손실 함수와 optimizer 설정
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 데이터로더 생성
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=batch_size)
    test_loader = DataLoader(test_data, batch_size=batch_size)

    # train(model, train_loader, val_loader, val_y, optimizer, criterion, device,
    #       num_epochs, 1, patience, batch_size, save_path="./results/save_model")

    model.load_state_dict(torch.load("./results/save_model/LSTM_postprocessing_best_model.pt"))
    #
    # test_loss = evaluate(model, test_loader, test_y, criterion, batch_size, device)
    # print(f'Test Loss: {test_loss:.3f} | Test PPL: {math.exp(test_loss):.3f}')
    translate_sentence(test_loader, test_y,  batch_size, model, device, max_len)
    # inference(test_loader, batch_size, model)

if __name__ == '__main__':
    main()