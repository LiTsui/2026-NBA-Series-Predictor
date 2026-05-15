from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
import pandas as pd
import torch
import torch.nn as nn

"""
Goal is to accurately make predictions based on training and validation data.
------------------------------------------------------------------
Using the 80-10-10 rule:
  Training:   1996-2019 (23 years)
  Validation: 2020-2021 (2 years) — 2020 Bubble may skew results
  Test:       2022-2025 (4 years)
"""


def convert(df, label):
    return torch.tensor(df[label].to_numpy(), dtype=torch.float32)


class SeriesNet(nn.Module):
    def __init__(self):
        super().__init__()

        # neural network layers
        self.net = nn.Sequential(
            nn.Linear(22, 64),  # 22 columns become 64 calculated values (neurons)
            nn.BatchNorm1d(64),  # normalize all 64 linear outputs
            nn.LeakyReLU(),  # lets negative values be used
            nn.Dropout(0.2),  # randomly disable 20% of the 64 neurons to reduce overfitting
            nn.Linear(64, 32),  # compress 64 values to 32 important values
            nn.BatchNorm1d(32),
            nn.LeakyReLU(),
            nn.Linear(32, 1),  # outputs a float in range [0, 1]
            nn.Sigmoid(),  # outputs a probability in range [0, 1]
        )

    def forward(self, x):
        return self.net(x)


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

    model = SeriesNet()

    # necessary in order to normalize all features onto the same scale
    scaler = StandardScaler()
    train_df[STATS] = scaler.fit_transform(train_df[STATS])
    valid_df[STATS] = scaler.transform(valid_df[STATS])

    # training and label data
    X_train = convert(train_df, STATS)
    y_train = convert(train_df, "LABEL").unsqueeze(1)

    # validation data set
    X_valid = convert(valid_df, STATS)
    y_valid = convert(valid_df, "LABEL").unsqueeze(1)

    # convert training and label data into tensordata and create 16 random batches of the data
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

    # binary loss function that compares actual output label vs predicted output label
    criterion = nn.BCELoss()

    # use to adjust parameters of the model in each iteration
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)  # lr is the learning rate

    # repeats for a certain amount of epochs for the model to repeatedly adjust
    for epoch in range(100):
        model.train()
        total_loss = 0  # error across all batches
        correct_train = 0
        total_train = 0

        # TRAINING DATA BATCHES
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()  # clear old gradients
            output = model(X_batch)  # make predictions
            loss = criterion(output, y_batch)  # compute error between predicted and actual
            loss.backward()  # recompute gradients
            optimizer.step()  # update weights
            total_loss += loss.item()  # add the loss percentage [0, 1] of each batch

            pred_train = (output >= 0.5).float()  # threshold at 0.5 where anything greater than 0.5 is 1 and anything less is 0
            correct_train += ((pred_train == y_batch).float().sum().item())  # number of all training data rows predicted correctly
            total_train += y_batch.size(0)  # total rows from all batches

        # percentage of training data rows predicted correctly in the epoch
        train_acc = correct_train / total_train

        # VALIDATION DATA
        model.eval()  # evaluation mode of model to test accuracy of the model
        with torch.no_grad():  # turn off gradients for evaluation mode

            output = model(X_valid)  # outputs probabilities in range [0, 1]

            pred_val = (output >= 0.5).float()
            val_acc = (pred_val == y_valid).float().mean().item()

        print(f"Epoch {epoch+1}/100 | Loss: {total_loss/len(train_loader):.4f} | Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")


if __name__ == "__main__":
    main()
