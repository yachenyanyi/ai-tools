from transformers import AutoModelForCausalLM
import torch
# 加载 Qwen 模型
model_name = "Qwen/Qwen2.5-1.5B"
qwen_model = AutoModelForCausalLM.from_pretrained(model_name)

# 获取模型的 Transformer 层列表
layers = qwen_model.model.layers  # 这是一个 torch.nn.ModuleList
#print(layers)
decoder_layer = qwen_model.model.layers[0]
#print(decoder_layer)
#qwen_model=[]
random_tensor = torch.randn(9, 6, 1536)
aa=decoder_layer(random_tensor)
aac=input()
print(aa[0].shape)