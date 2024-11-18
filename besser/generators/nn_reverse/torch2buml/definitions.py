"""
Module containing lookup dictionaries for transforming PyTorch code
to BUML code.
"""

lookup_layers = {
    "Conv1d": "Conv1D", "Conv2d": "Conv2D", "Conv3d": "Conv3D",           
    "MaxPool1d": "PoolingLayer", "MaxPool2d": "PoolingLayer", 
    "MaxPool3d": "PoolingLayer", "AvgPool1d": "PoolingLayer", 
    "AvgPool2d": "PoolingLayer", "AvgPool3d": "PoolingLayer",
    "AdaptiveAvgPool1d": "PoolingLayer", "AdaptiveAvgPool2d": "PoolingLayer", 
    "AdaptiveAvgPool3d": "PoolingLayer", "AdaptiveMaxPool1d": "PoolingLayer", 
    "AdaptiveMaxPool2d": "PoolingLayer", "AdaptiveMaxPool3d": "PoolingLayer", 
    "Flatten": "FlattenLayer", "Linear": "LinearLayer", 
    "Embedding": "EmbeddingLayer", "BatchNorm1d": "BatchNormLayer", 
    "BatchNorm2d": "BatchNormLayer", "BatchNorm3d": "BatchNormLayer",
    "LayerNorm": "LayerNormLayer", "Dropout": "DropoutLayer", 
    "RNN": "SimpleRNNLayer", "LSTM": "LSTMLayer", "GRU": "GRULayer"
}

lookup_actv_fun = {
    "ReLU": "relu", "LeakyReLU": "leaky_relu", "Sigmoid": "sigmoid",
    "Softmax": "softmax", "Tanh": "tanh"
}

lookup_layers_params = {
    "in_channels": "in_channels", "out_channels": "out_channels",
    "kernel_size": "kernel_dim", "stride": "stride_dim", 
    "padding": "padding_amount", "output_size": "output_dim", 
    "input_size": "input_size", "hidden_size": "hidden_size", 
    "bidirectional": "bidirectional", "dropout": "dropout", 
    "batch_first": "batch_first", "normalized_shape": "normalized_shape", 
    "p": "rate", "num_features": "num_features", 
    "num_embeddings": "num_embeddings", "embedding_dim": "embedding_dim", 
    "start_dim": "start_dim", "end_dim": "end_dim", 
    "in_features": "in_features", "out_features": "out_features",
    "return_type": "return_type", "permute_dim": "permute_dim"
}

layers_fixed_params = {
    "MaxPool1d": {"pooling_type": "max", "dimension": "1D"},
    "MaxPool2d": {"pooling_type": "max", "dimension": "2D"},
    "MaxPool3d": {"pooling_type": "max", "dimension": "3D"},
    "AvgPool1d": {"pooling_type": "avg", "dimension": "1D"},
    "AvgPool2d": {"pooling_type": "avg", "dimension": "2D"},
    "AvgPool3d": {"pooling_type": "avg", "dimension": "3D"},
    "AdaptiveAvgPool1d": {"pooling_type": "adaptive_average", 
                          "dimension": "1D"},
    "AdaptiveAvgPool2d": {"pooling_type": "adaptive_average", 
                          "dimension": "2D"},
    "AdaptiveAvgPool3d": {"pooling_type": "adaptive_average", 
                          "dimension": "3D"},
    "AdaptiveMaxPool1d": {"pooling_type": "adaptive_max", "dimension": "1D"},
    "AdaptiveMaxPool2d": {"pooling_type": "adaptive_max", "dimension": "2D"},
    "AdaptiveMaxPool3d": {"pooling_type": "adaptive_max", "dimension": "3D"},
    "BatchNorm1d": {"dimension": "1D"},
    "BatchNorm2d": {"dimension": "2D"},
    "BatchNorm3d": {"dimension": "3D"},
}

rnn_cnn_layers = ["LSTM", "GRU", "SimpleRNN",
                  "Conv1d", "Conv2d", "Conv3d"]

config_list = ["batch_size", "epochs", "learning_rate",
               "optimizer", "metrics", "loss_function"]

train_param_list = ["name", "path_data", "task_type", "input_format"]
test_param_list = ["name", "path_data"]

lookup_loss_func = {"CrossEntropyLoss": "crossentropy",
                    "BCELoss": "binary_crossentropy",
                    "MSELoss": "mse"}