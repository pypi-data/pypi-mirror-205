"""Pytorch Models for sequentail data (non-iid rows or time/step dependence
        NNs for multi-row inputs and multiple(one row) output
        Train-one fit all with new samples using Dataloaders.
        Implement, LSTM and variations of transformers.
        See demo pt III
	Includes:
	
	create_sequences(data_seq_len) to build (without flattening n days, m vars) the X,y tensors. For 1 day per prediction, dimension of y is n*m
	create_n_seq_ts(data, seq_len, id_split) gives X,y,Xt,yt for train test split on i_split

	modelList_torch_ts - a modellist 
		this contains LSTM and Transformers (vanilla) so far which need the torch.nn, torch.optim. Note that nn.Transformer, nn.LSTM are called

	create_objective_ts(model_class, cv, tune_grid, opt_params, data, device, seq_len)
	  - returns an objective() for optuna.

	tscv = TimeSeriesSplit(n_splits=3)

objective = create_objective_ts(LSTM,tscv,lstm_grid,opt_grid,data,device, seq_len)

study = optuna.create_study(direction='minimize', pruner=optuna.pruners.MedianPruner())
study.optimize(objective, n_trials=100)	
	then, refer to the study object in Optuna.


	Speed: can be improved by using cuda or CPU parallel.
	With a short test cuda on 3090 is 3.5x the speed of i9 13900K on Z690
	Please follow the project for other benchmarks.
	...
	
	Troubleshooting of CUDA, pls use 
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

	But note that most errors of values or memories are about the
dimension mismatch of the model class


        

"""


modelList_torch_tsRegressor = []


def ts_aggregate_flatten(X, n_order, n_forward = 1, flatten_predictor = False, flatten_target = True):
    return null



def create_sequences(data, seq_len):
    X = []
    y = []
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i,:])
        y.append(data[i, :])
    X_tensor = torch.stack(X)
    y_tensor = torch.stack(y) # stack the tensors in y into a single tensor
    return X_tensor, y_tensor

def create_n_seq_ts(data,seq_len,id_split):
    """
    #seq_len=5
    #x,y,xt,yt = create_n_seq_ts(data,seq_len,90)
    """
    X,y = create_sequences(data=data,seq_len=seq_len)
    
    return X[0:id_split,:], y[0:id_split,:], X[id_split:,:], y[id_split:,:]



import optuna
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import TimeSeriesSplit



# Define LSTM model
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        output, _ = self.lstm(x)
        output = self.linear(output[:, -1, :])
        return output

# Define tuning grids
lstm_grid = {
    "num_layers": (1, 3),
    "hidden_size": (10, 100),
}

opt_grid = {
    "batch_size" : (8,16),
    "learning_rate": (1e-5, 1e-1),
    "num_epochs" : (100,150)
}

nVar = y.shape[1]

import torch
import optuna
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from torch.utils.data import DataLoader, TensorDataset


def create_objective_ts(model_class, cv, tune_grid, opt_params,data, device, seq_len):
    """
    Returns an objective() function to be optimized by Optuna

    tscv = TimeSeriesSplit(n_splits=3)

    objective = create_objective_ts(LSTM,tscv,lstm_grid,opt_grid,data,device, seq_len)

    study = optuna.create_study(direction='minimize', pruner=optuna.pruners.MedianPruner())
    study.optimize(objective, n_trials=100)

    # Print best hyperparameters and loss
    print('Best hyperparameters:', study.best_params)
    print('Best loss:', study.best_value)


"""
    def objective(trial):
        # Sample hyperparameters from tuning grid
        params = {param_name: trial.suggest_categorical(param_name, param_values) 
                  for param_name, param_values in tune_grid.items()}
        params['input_size'] = nVar
        params['output_size'] = nVar
        # Initialize model
        model = model_class(**params)
        model.to(device)
        
        # Define loss function and optimizer
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=trial.suggest_categorical('learning_rate',opt_params['learning_rate']))
        
        num_epochs = trial.suggest_categorical('num_epochs',opt_params['num_epochs'])
        batch_size = trial.suggest_categorical('batch_size',opt_params['batch_size'])
        
        # Train and evaluate model using cross-validation
        val_losses = []
        for train_idx, val_idx in cv.split(data):

            id_split = val_idx[0]
            
            train_X_fold, train_y_fold, val_X_fold, val_y_fold = create_n_seq_ts(data[:val_idx[-1]+1,:],seq_len,id_split)
            train_X_fold = train_X_fold[train_idx[0]:]
            train_y_fold = train_y_fold[train_idx[0]:]
            train_dataset = TensorDataset(train_X_fold.float(), 
                                          train_y_fold.float())#.to(device)
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

            val_dataset = TensorDataset(val_X_fold.float(), 
                                        val_y_fold.float())#.to(device)
            val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)# only load 1 entry of data to predict next 1 day
            
            
            for epoch in range(num_epochs):
                # Train model
                model.train()
                for inputs, targets in train_loader:
                    inputs = inputs.to(device)
                    targets = targets.to(device)
                    
                    optimizer.zero_grad()
                    
                    outputs = model(inputs)
                    
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()

                # Evaluate model on validation set
                model.eval()
                with torch.no_grad():
                    val_loss = 0
                    for inputs, targets in val_loader:
                        inputs = inputs.to(device)
                        targets = targets.to(device)

                        outputs = model(inputs)
                        val_loss += criterion(outputs, targets).item()
                    val_loss /= len(val_loader)
                    val_losses.append(val_loss)

                trial.report(val_loss, epoch)
                # Prune if necessary
                if trial.should_prune():
                    raise optuna.exceptions.TrialPruned()
        
        loss_score = float(np.mean(val_losses))
        return loss_score
    return objective

modelList_torch_tsRegressor.append({"modelInit": LSTM,
                                    "par": lstm_grid,
                                    "opt" = opt_grid})




# Transformer for multivar time series, ordered n, predict 1 day per iteration


class TransformerModel(nn.Module):

    def __init__(self, input_size, output_size, n_heads, n_layers, dropout):
        super(TransformerModel, self).__init__()

        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=input_size,
                nhead=n_heads,
                dropout=dropout
            ),
            num_layers=n_layers
        )
        self.decoder = nn.Linear(input_size, output_size)

    def forward(self, x):
        x = self.transformer_encoder(x)
        x = self.decoder(x[:, -1, :])
        return x

transformer_grid = {"n_heads" :[2],
                    "n_layers" : [2,4,6,8],
                    "dropout" : [.1,.2]}

modelList_torch_tsRegressor.append({"modelInit": TransformerModel,
                                    "par": transformer_grid,
                                    "opt" = opt_grid})






