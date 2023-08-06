from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import numpy as np


def calculate_regression_metrics(model, x_val, y_true):
    y_pred = model.predict(x_val)

    metrics = {
        'mae': mean_absolute_error(y_true, y_pred),
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2score': r2_score(y_true, y_pred),
        'mape': mean_absolute_percentage_error(y_true, y_pred),
    }

    return metrics


def calculate_classification_metrics(model, x_val, y_true, average=None):
    y_pred_prob = model.predict(x_val)
    y_pred = np.argmax(y_pred_prob, axis=-1)

    if len(np.unique(y_true)) > 2:
        # 다중 클래스 분류
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=average)
        recall = recall_score(y_true, y_pred, average=average)
        f1score = f1_score(y_true, y_pred, average=average)
    else:
        # 이진 분류
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=average, pos_label=1)
        recall = recall_score(y_true, y_pred, average=average, pos_label=1)
        f1score = f1_score(y_true, y_pred, average=average, pos_label=1)

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1score': f1score
    }

    return metrics
