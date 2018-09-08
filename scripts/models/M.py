import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm

class M(nn.Module):
	def __init__(self, input_size, output_size):
		super(M, self).__init__()
		self.input_size = input_size
		self.output_size = output_size
		self.embedding = nn.Linear(input_size, output_size)

	def forward(self, v, a1, a2):
		embedded = self.embedding(v)
		output1 = torch.dot(embedded, a1)
		output2 = torch.dot(embedded, a2)
		return output1, output2

def train(save_path, log, form, dep, lang, examples, dim, batch, epoch):
	log.write("M_{}_{}_{}_{}_{}_{}:\n".format(form, dep, lang, dim, batch, epoch))
	model = M(dim, dim)
	optimizer = optim.SGD(model.parameters(), lr = 0.1)
	for num in range(epoch):
		print("epoch " + str(num))
		log.write("epoch\t" + str(num) + ":\n")
		loss = 0
		cnt = 0
		for i in tqdm(range(len(examples))):
			v, a1, a2 = examples[i]
			output1, output2 = model.forward(v, a1, a2)
			loss += F.relu(1 + output2 - output1)
			cnt += 1
			if cnt == batch or i == len(examples) - 1:
				loss.backward()
				optimizer.step()
				log.write("loss:\t" + str(loss) + "\n")
				print("loss:\t" + str(loss))
				optimizer.zero_grad()
				loss = 0
				cnt = 0
	torch.save(model, (save_path / "M_{}_{}_{}_{}_{}_{}".format(form, dep, lang, dim, batch, epoch)))
	return model.embedding
