from sentence_transformers import SentenceTransformer,util
import torch
import pdb
model = SentenceTransformer('indiejoseph/bert-cantonese-sts')
sentences = ['Lack of saneness',
        'Absence of sanity',
        'A man is eating food.',
        'A man is eating a piece of bread.',
        'The girl is carrying a baby.',
        'A man is riding a horse.',
        'A woman is playing violin.',
        'Two men pushed carts through the woods.',
        'A man is riding a white horse on an enclosed ground.',
        'A monkey is playing drums.',
        'A cheetah is running behind its prey.']
sentence_embeddings = model.encode(sentences)
short_emb=model.encode(['A woman is playing violin.'])
for sentence, embedding in zip(sentences, sentence_embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

similarities = util.pytorch_cos_sim(short_emb, sentence_embeddings)
most_similar_idx = torch.argmax(similarities).item()
pdb.set_trace()