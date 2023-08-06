import torch
import torch.nn as nn


class GANGenerator(nn.Module):
    """GAN生成器模型"""
    def __init__(self, input_size: int, output_size: int, hidden_size: int):
        """

        :param input_size: 输入向量的维度
        :param output_size: 输出向量的维度
        :param hidden_size: 隐藏层的维度
        """
        super(GANGenerator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Tanh()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model(x)
        return x


class GANDiscriminator(nn.Module):
    """GAN判别器模型"""
    def __init__(self, input_size: int, hidden_size: int):
        """

        :param input_size: 输入向量的维度
        :param hidden_size: 隐藏层的维度
        """
        super(GANDiscriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model(x)
        return x
