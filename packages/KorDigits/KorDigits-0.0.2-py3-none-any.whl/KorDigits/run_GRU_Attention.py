import re
import time
import datetime
import pandas as pd
import gc

import torch
import torch.optim as optim
import torch.nn.functional as F
from tqdm.auto import tqdm
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils import clip_grad_norm_

from utils.KoCharELECTRA.tokenization_kocharelectra import KoCharElectraTokenizer
from model.GRU_Attention_model import Encoder, Attention, Decoder, Seq2Seq

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


def evaluate(model, val_iter, target, vocab_size, batch_size):
    start = time.time()
    total = len(val_iter) * batch_size
    total_correct = 0
    pbar = tqdm(val_iter, desc="Val", dynamic_ncols=True)
    with torch.no_grad():
        model.eval()
        total_loss = 0
        for b, batch in enumerate(pbar):
            src, trg = batch
            src = [[row[i] for row in src] for i in range(len(src[0]))]
            trg = [[[row[i] for row in trg] for i in range(len(trg[0]))]]

            src = torch.LongTensor(src).squeeze(0)
            trg = torch.LongTensor(trg).squeeze(0)

            src = src.data.to(device)
            trg = trg.data.to(device)

            trg_word = target[b * batch_size: (b + 1) * batch_size]

            output = model(src, trg, teacher_forcing_ratio=0.0)

            loss = F.nll_loss(output[1:].view(-1, vocab_size),
                              trg[1:].contiguous().view(-1),
                              ignore_index=0)
            total_loss += loss.data.item()
            try:
                # acc
                for i in range(batch_size):
                    # 412 = [, 413 = ]
                    preds = output.argmax(dim=-1).cpu().numpy()
                    preds = preds[:, i]
                    # print(preds.shape)
                    # print(batch_size)
                    # print()
                    true = trg[:, i].cpu().numpy()
                    pred = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in preds],
                                            skip_special_tokens=True)
                    true_decode = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in true],
                                            skip_special_tokens=True)
                    if all(preds == true):
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
            except:
                pass
            pbar.set_description(f"Val Loss: {loss.data.item()}, Acc: {total_correct}/{total}: {total_correct/total}")
        end = time.time()
        sec = (end - start)
        result = datetime.timedelta(seconds=sec)
        print("time:", result)
        return total_loss / len(val_iter)


def train(e, model, optimizer, train_iter, vocab_size, grad_clip, batch_size):
    model.train()
    total_loss = 0
    pbar = tqdm(train_iter, desc="Train", dynamic_ncols=True)
    for b, batch in enumerate(pbar):
        src, trg = batch
        src = [[row[i] for row in src] for i in range(len(src[0]))]
        trg = [[[row[i] for row in trg] for i in range(len(trg[0]))]]

        src = torch.LongTensor(src).squeeze(0)
        trg = torch.LongTensor(trg).squeeze(0)
        src, trg = src.to(device), trg.to(device)
        optimizer.zero_grad()
        output = model(src, trg)
        loss = F.nll_loss(output[1:].view(-1, vocab_size),
                          trg[1:].contiguous().view(-1),
                          ignore_index=0)

        pbar.set_description(f"Train Loss : {loss.data.item()} ")
        loss.backward()
        clip_grad_norm_(model.parameters(), grad_clip)
        optimizer.step()
        total_loss += loss.data.item()


        # if b % 100 == 0 and b != 0:
        #     total_loss = total_loss / 100
        #     print("[%d][loss:%5.2f][pp:%5.2f]" %
        #           (b, total_loss, math.exp(total_loss)))
        #     total_loss = 0
    print("Train Loss:",total_loss/(len(train_iter) * batch_size))


def generate(model, val_iter, target, vocab_size, batch_size):
    total = len(val_iter) * batch_size
    total_correct = 0
    pbar = tqdm(val_iter, desc="Val", dynamic_ncols=True)

    df_wrong = pd.DataFrame(columns=['Source', 'Target', 'Prediction'])
    df_correct = pd.DataFrame(columns=['Source', 'Target', 'Prediction'])

    with torch.no_grad():
        model.eval()
        total_loss = 0
        for b, batch in enumerate(pbar):
            src, trg = batch
            src = [[row[i] for row in src] for i in range(len(src[0]))]
            trg = [[[row[i] for row in trg] for i in range(len(trg[0]))]]

            src = torch.LongTensor(src).squeeze(0)
            trg = torch.LongTensor(trg).squeeze(0)

            src = src.data.to(device)
            trg = trg.data.to(device)

            trg_word = target[b * batch_size: (b + 1) * batch_size]

            output = model(src, trg, teacher_forcing_ratio=0.0)

            loss = F.nll_loss(output[1:].view(-1, vocab_size),
                              trg[1:].contiguous().view(-1),
                              ignore_index=0)
            total_loss += loss.data.item()
            try:
                # acc
                for i in range(batch_size):
                    # 412 = [, 413 = ]
                    preds = output.argmax(dim=-1).cpu().numpy()
                    preds = preds[:, i]
                    # print(preds.shape)
                    # print(batch_size)
                    # print()
                    true = trg[:, i].cpu().numpy()
                    source = tokenizer.decode(src[:, i], skip_special_tokens=True)
                    pred = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in preds],
                                            skip_special_tokens=True)
                    true_decode = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in true],
                                            skip_special_tokens=True)

                    if all(preds == true):
                        total_correct += 1
                        df_correct = df_correct.append({"Source": source, "Target": true_decode, "Prediction": pred},
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
                            df_wrong = df_wrong.append({"Source": source, "Target": true_decode, "Prediction": pred},
                                                       ignore_index=True)
                            continue

                        if is_equal:
                            total_correct += 1
                            df_correct = df_correct.append(
                                {"Source": source, "Target": true_decode, "Prediction": pred},
                                ignore_index=True)
                        else:
                            df_wrong = df_wrong.append({"Source": source, "Target": true_decode, "Prediction": pred},
                                                       ignore_index=True)
            except:
                pass
            pbar.set_description(f"Val Loss: {loss.data.item()}, Acc: {total_correct}/{total}: {total_correct/total}")

        # 결과 저장
        df_correct.to_csv("./results/correct_attn.csv", index=False, encoding='utf-8-sig')
        df_wrong.to_csv("./results/wrong_attn.csv", index=False, encoding='utf-8-sig')

        return total_loss / len(val_iter)

def main():
    epochs = 100
    batch_size = 16
    lr = 0.0001
    grad_clip = 10.0
    hidden_size = 512
    embed_size = 256
    max_len = 128
    patience = 3
    early_stop_count = 0
    print(device)
    print("[!] preparing dataset...")
    train_data = TranslationDataset("utils/special_window_train.txt", max_len)
    val_data = TranslationDataset("utils/special_window_val.txt", max_len)
    test_data = TranslationDataset("utils/special_window_test.txt", max_len)

    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=batch_size)
    test_loader = DataLoader(test_data, batch_size=batch_size)

    train_y = TargetDataset("utils/special_window_train_target.txt", max_len)
    val_y = TargetDataset("utils/special_window_val_target.txt", max_len)
    test_y = TargetDataset("utils/special_window_test_target.txt", max_len)

    src_size = tokenizer.vocab_size + 2

    print("[!] Instantiating models...")
    encoder = Encoder(src_size, embed_size, hidden_size,
                      n_layers=2, dropout=0.5)
    decoder = Decoder(embed_size, hidden_size, src_size,
                      n_layers=1, dropout=0.5)
    seq2seq = Seq2Seq(encoder, decoder).to(device)
    optimizer = optim.Adam(seq2seq.parameters(), lr=lr)
    print(seq2seq)

    best_val_loss = None
    torch.cuda.empty_cache()
    gc.collect()
    # for e in range(1, epochs + 1):
    #     train(e, seq2seq, optimizer, train_loader,
    #           src_size, grad_clip, batch_size)
    #     val_loss = evaluate(seq2seq, val_loader, val_y, src_size, batch_size)
    #     print("[Epoch:%d] val_loss:%5.3f | val_pp:%5.2fS"
    #           % (e, val_loss, math.exp(val_loss)))
    #
    #     # Save the model if the validation loss is the best we've seen so far.
    #     if not best_val_loss or val_loss < best_val_loss:
    #         print("[!] saving model...")
    #         if not os.path.isdir("results/save_model"):
    #             os.makedirs("results/save_model")
    #         torch.save(seq2seq.state_dict(), 'results/save_model/seq2seq_%d.pt' % (e))
    #         best_val_loss = val_loss
    #     else:
    #         early_stop_count += 1
    #         print("early_stop_count: ",early_stop_count)
    #         if early_stop_count >= patience:
    #             print(f"Validation loss didn't improve for {patience} epochs. Training stopped.")
    #             break

    seq2seq.load_state_dict(torch.load("results/save_model/seq2seq_5.pt"))
    test_loss = evaluate(seq2seq, test_loader, test_y, src_size, batch_size)
    print("[TEST] loss:%5.2f" % test_loss)


if __name__ == '__main__':
    main()