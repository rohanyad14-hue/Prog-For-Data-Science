"""Notes M2: gradient descent by hand vs autograd, activations, and minimal Keras / PyTorch / TensorFlow / XGBoost use."""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf
import torch
import xgboost as xgb
import keras
from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.model_selection import train_test_split

print("=== one gradient-descent step by hand: y = w*x + b, MSE loss ===")
x = np.array([1.0, 2.0, 3.0]); y = np.array([2.0, 4.0, 6.0])
w, b, lr = 0.0, 0.0, 0.1
pred = w * x + b
loss = np.mean((pred - y) ** 2)
dw = np.mean(2 * (pred - y) * x)
db = np.mean(2 * (pred - y))
print(f"pred={pred.tolist()} loss=mean((pred-y)^2)={loss:.4f}")
print(f"dL/dw = mean(2(pred-y)x) = {dw:.4f} | dL/db = mean(2(pred-y)) = {db:.4f}")
print(f"update: w = w - lr*dL/dw = {w - lr * dw:.4f} | b = b - lr*dL/db = {b - lr * db:.4f}")
tw, tb = torch.tensor(0.0, requires_grad=True), torch.tensor(0.0, requires_grad=True)
tx, ty = torch.tensor(x), torch.tensor(y)
l = ((tw * tx + tb - ty) ** 2).mean()
l.backward()
print(f"PyTorch autograd : dL/dw = {tw.grad.item():.4f}, dL/db = {tb.grad.item():.4f}")
vw, vb = tf.Variable(0.0), tf.Variable(0.0)
with tf.GradientTape() as tape:
    lt = tf.reduce_mean((vw * x + vb - y) ** 2)
gw, gb = tape.gradient(lt, [vw, vb])
print(f"TensorFlow tape  : dL/dw = {gw.numpy():.4f}, dL/db = {gb.numpy():.4f}")
print("trap: PyTorch accumulates gradients - calling backward() twice without zero_grad():")
tw2 = torch.tensor(1.0, requires_grad=True)
for _ in range(2):
    (tw2 * 3).backward()
print("   grad after two backward calls =", tw2.grad.item(), "(should be 3 each time -> 6 means accumulation)")

print("\n=== activations ===")
z = np.array([1.0, 2.0, 3.0])
print("sigmoid(0) =", 1 / (1 + np.exp(0)), "| relu([-2, 3]) =", np.maximum(0, [-2, 3]).tolist(), "| tanh(0) =", np.tanh(0))
sm = np.exp(z) / np.exp(z).sum()
print("softmax([1,2,3]) =", sm.round(4).tolist(), "sums to", round(float(sm.sum()), 4), "-> class probabilities")

print("\n=== Keras (Sequential API): 4 inputs -> Dense(8, relu) -> Dense(3, softmax) ===")
keras.utils.set_random_seed(0)
Xi, yi = load_iris(return_X_y=True)
Xi = (Xi - Xi.mean(0)) / Xi.std(0)
model = keras.Sequential([keras.layers.Input(shape=(4,)), keras.layers.Dense(8, activation="relu"), keras.layers.Dense(3, activation="softmax")])
print("params layer 1 = 4*8 + 8 =", 4 * 8 + 8, "| layer 2 = 8*3 + 3 =", 8 * 3 + 3, "| model.count_params() =", model.count_params())
model.compile(optimizer=keras.optimizers.Adam(0.05), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
hist = model.fit(Xi, yi, epochs=30, batch_size=16, verbose=0)
print(f"loss {hist.history['loss'][0]:.3f} -> {hist.history['loss'][-1]:.3f} | accuracy {hist.history['accuracy'][0]:.2f} -> {hist.history['accuracy'][-1]:.2f}")
print("predict output shape:", model.predict(Xi[:2], verbose=0).shape, "(one probability per class)")
print("one epoch = a pass over all 150 rows; with batch_size=16 that is", int(np.ceil(150 / 16)), "weight updates per epoch")

print("\n=== PyTorch: the explicit training loop ===")
torch.manual_seed(0)
net = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.ReLU(), torch.nn.Linear(8, 3))
opt = torch.optim.Adam(net.parameters(), lr=0.05)
lossf = torch.nn.CrossEntropyLoss()
Xt = torch.tensor(Xi, dtype=torch.float32)
yt = torch.tensor(yi, dtype=torch.long)       # CrossEntropyLoss needs int64 class labels; int32 raises a RuntimeError
first = None
for epoch in range(30):
    opt.zero_grad()                 # 1 clear old gradients
    out = net(Xt)                   # 2 forward pass
    loss = lossf(out, yt)           # 3 loss
    loss.backward()                 # 4 backpropagation
    opt.step()                      # 5 weight update
    first = first if first is not None else loss.item()
print(f"loss {first:.3f} -> {loss.item():.3f} | accuracy {(net(Xt).argmax(1) == yt).float().mean().item():.2f} | parameters {sum(p.numel() for p in net.parameters())}")

print("\n=== TensorFlow tensors and shapes ===")
t = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print("tf.matmul:", tf.matmul(t, t).numpy().tolist(), "| shape", t.shape, "| dtype", t.dtype.name, "| numpy interop:", type(t.numpy()).__name__)

print("\n=== XGBoost: boosting adds trees that fix the previous errors ===")
Xc, yc = load_breast_cancer(return_X_y=True)
Xa, Xb, ya, yb = train_test_split(Xc, yc, test_size=0.3, random_state=0, stratify=yc)
for n in (1, 10, 100):
    m = xgb.XGBClassifier(n_estimators=n, max_depth=3, learning_rate=0.3, random_state=0).fit(Xa, ya)
    print(f"n_estimators={n:<4} test accuracy={m.score(Xb, yb):.3f}")
names = load_breast_cancer().feature_names
top = np.argsort(m.feature_importances_)[::-1][:3]
print("top features:", [str(names[i]) for i in top])
Xt2, Xv, yt2, yv = train_test_split(Xa, ya, test_size=0.25, random_state=0, stratify=ya)      # validation set carved from TRAIN
m2 = xgb.XGBClassifier(n_estimators=500, learning_rate=0.1, early_stopping_rounds=10, eval_metric="logloss", random_state=0).fit(Xt2, yt2, eval_set=[(Xv, yv)], verbose=False)
print("early stopping: best tree =", m2.best_iteration, "of 500 allowed | untouched test accuracy:", round(m2.score(Xb, yb), 3), "(never use the test set for early stopping)")
