import torch

# 检查是否有可用的 CUDA 设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# 创建两个向量，并移动到 GPU
a = torch.tensor([1.0, 2.0, 3.0], device=device)
b = torch.tensor([4.0, 5.0, 6.0], device=device)

# 1. 向量加法
c = a + b
print("向量加法:", c)  # 输出在 GPU 上的张量

# 2. 点积（内积）
dot_product = torch.dot(a, b)
print("点积:", dot_product.item())  # .item() 转为 Python 标量

# 3. L2 范数
norm_a = torch.norm(a)
print("L2 范数:", norm_a.item())

# 4. 余弦相似度
cos_sim = torch.dot(a, b) / (torch.norm(a) * torch.norm(b))
print("余弦相似度:", cos_sim.item())

# 5. 逐元素相乘
elementwise = a * b
print("逐元素相乘:", elementwise)

# （可选）把结果移回 CPU 并转为 NumPy
if device.type == 'cuda':
    print("\n转为 NumPy（需先移回 CPU）:")
    print("加法结果 (NumPy):", c.cpu().numpy())