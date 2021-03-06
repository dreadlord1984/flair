from flair.data import NLPTaskDataFetcher, TaggedCorpus, NLPTask
from flair.embeddings import TextEmbeddings, WordEmbeddings, StackedEmbeddings, CharLMEmbeddings, CharacterEmbeddings
from typing import List
import torch

# 1. get the corpus
corpus: TaggedCorpus = NLPTaskDataFetcher.fetch_data(NLPTask.CONLL_03).downsample(0.1)
print(corpus)

# 2. what tag do we want to predict?
tag_type = 'ner'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)

# initialize embeddings
embedding_types: List[TextEmbeddings] = [

    WordEmbeddings('glove')

    # comment in this line to use character embeddings
    # , CharacterEmbeddings()

    # comment in these lines to use contextual string embeddings
    # ,
    # CharLMEmbeddings('news-forward')
    # ,
    # CharLMEmbeddings('news-backward')
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# initialize sequence tagger
from flair.tagging_model import SequenceTaggerLSTM

tagger: SequenceTaggerLSTM = SequenceTaggerLSTM(hidden_size=256, embeddings=embeddings, tag_dictionary=tag_dictionary,
                                                use_crf=True)
if torch.cuda.is_available():
    tagger = tagger.cuda()

# initialize trainer
from flair.trainer import TagTrain

trainer: TagTrain = TagTrain(tagger, corpus, tag_type=tag_type, test_mode=True)

trainer.train('resources/taggers/example-pos', mini_batch_size=32, max_epochs=150, save_model=False,
              train_with_dev=False, anneal_mode=False)
