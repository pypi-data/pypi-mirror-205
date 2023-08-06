import torch
from torchgan import models

input_size = 100
output_size = 784
hidden_size = 256

generator = models.GANGenerator(input_size, output_size, hidden_size)
input_vector = torch.randn(1, input_size)
generated_sample = generator(input_vector)

print(generated_sample)

d = models.GANDiscriminator(output_size, hidden_size)
d_output = d(generated_sample)
print(d_output)
