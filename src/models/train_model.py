from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
from src.utils import h
import pandas as pd
import torch.nn as nn
import torch
import joblib

"""
Use training data to train the model. 
Predict playoff series outcomes based on validation data.
------------------------------------------------------------------
Using the 80-10-10 rule:
  Training:   1996-2019 (23 years)
  Validation: 2020-2021 (2 years) — 2020 Bubble may skew results
  Test:       2022-2025 (4 years)
"""


class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()

        # neural network layers
        self.net = nn.Sequential(
            nn.Linear(22, 100),  # 22 columns to 100 calculated values (neurons)
            nn.BatchNorm1d(100),  # normalize all 100 neurons
            nn.LeakyReLU(),  # lets negative values be used
            nn.Dropout(0.75),  # randomly disable 75% of the 100 neurons to reduce overfitting
            nn.Linear(100, 32),  # compress 100 to 32 neurons
            nn.BatchNorm1d(32),
            nn.Linear(32, 1),  # outputs a number from -inf to inf
            nn.Sigmoid(),  # converts number to a probability in range [0, 1]
        )

    def forward(self, x):
        return self.net(x)


def train(model, train_loader, X_valid, y_valid):
    # loss function that combines BCE and sigmoid; compares actual label vs predicted label
    criterion = nn.BCEWithLogitsLoss()

    # use to adjust parameters of the model in each iteration
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # lr is the learning rate

    best_val_acc = 0  # find the best epoch for validation accuracy

    # repeats for a certain amount of epochs for the model to repeatedly adjust
    for epoch in range(100):
        model.train()
        total_loss = 0  # error across all batches
        correct_train = 0
        total_train = 0
        train_acc = 0

        # TRAINING DATA BATCHES
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()  # clear old gradients
            noise = torch.randn_like(X_batch) * 0.05  # use noise to memorize patterns and not information
            output = model(X_batch + noise)  # make predictions
            loss = criterion(output, y_batch)  # compute error between predicted and actual
            loss.backward()  # recompute gradients
            optimizer.step()  # update weights
            total_loss += loss.item()  # add the loss percentage [0, 1] of each batch

            pred_train = (output >= 0.5).float()  # threshold at 0.5 where anything greater than 0.5 is 1 and anything less is 0
            correct_train += (pred_train == y_batch).float().sum().item()  # number of all training data rows predicted correctly
            total_train += y_batch.size(0)  # total rows from all batches

            train_acc = correct_train / total_train  # percentage of training data rows predicted correctly in the epoch

        # VALIDATION DATA TESTING
        model.eval()  # evaluation mode to test model accuracy
        with torch.no_grad():  # turn off gradients for evaluation mode

            output = model(X_valid)  # outputs probabilities in range [0, 1]

            pred_val = (output >= 0.5).float()
            val_acc = (pred_val == y_valid).float().mean().item()

            # h.actual_vs_pred(model, X_valid, y_valid, pred_val)

        # save the model when trained at most accurate epoch
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), "../data/model/best_model.pt")

        print(
            f"Epoch {epoch + 1}/100 | Loss: {total_loss / len(train_loader):.4f} | Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}"
        )

    print(f"\nBest Val Acc: {best_val_acc:.4f}")


def main():
    train_df = pd.read_csv("../data/training.csv")
    valid_df = pd.read_csv("../data/validation.csv")

    STATS = [
        "PointsPG_DIFF",
        "OppPointsPG_DIFF",
        "DiffPointsPG_DIFF",
        "E_OFF_RATING_DIFF",
        "OFF_RATING_DIFF",
        "E_DEF_RATING_DIFF",
        "DEF_RATING_DIFF",
        "E_NET_RATING_DIFF",
        "NET_RATING_DIFF",
        "AST_PCT_DIFF",
        "AST_TO_DIFF",
        "AST_RATIO_DIFF",
        "OREB_PCT_DIFF",
        "DREB_PCT_DIFF",
        "REB_PCT_DIFF",
        "TM_TOV_PCT_DIFF",
        "EFG_PCT_DIFF",
        "TS_PCT_DIFF",
        "E_PACE_DIFF",
        "PACE_DIFF",
        "PIE_DIFF",
        "H2H_WIN_RATIO",
    ]

    model = NeuralNet()

    # necessary in order to normalize all features onto the same scale
    scaler = StandardScaler()

    # scales and transforms data to fit training data
    train_df[STATS] = scaler.fit_transform(train_df[STATS])
    joblib.dump(scaler, "../data/model/scaler.pkl")

    # transforms validation data using fitted scaler data
    valid_df[STATS] = scaler.transform(valid_df[STATS])

    # training and label data
    X_train = h.convert(train_df, STATS)
    y_train = h.convert(train_df, "LABEL").unsqueeze(1)

    # validation data set
    X_valid = h.convert(valid_df, STATS)
    y_valid = h.convert(valid_df, "LABEL").unsqueeze(1)

    # convert training and label data into tensor data and create 32 random batches of the data
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    train(model, train_loader, X_valid, y_valid)

    # h.find_dropout(train_loader, X_valid, y_valid)
    # h.find_neurons(train_loader, X_valid, y_valid)


if __name__ == "__main__":
    main()
