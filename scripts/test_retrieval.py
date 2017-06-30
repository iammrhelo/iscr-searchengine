import argparse
import os
import sys
import time
sys.path.append('.')

import numpy as np
from tqdm import tqdm

from iscr.searchengine import SearchEngine
from iscr.searchengine.metrics import normalize, evalAP
from iscr.searchengine.utils import load_from_pickle

def run_ap_baseline(query_pickle, data_dir):

	lex_pickle = os.path.join(data_dir,'lex.pickle')
	index_pickle = os.path.join(data_dir,'indices.pickle')

	engine = SearchEngine(lex_pickle, index_pickle)

	query = load_from_pickle(query_pickle)

	_start_time = time.time()

	aps = []

	for query_idx in tqdm(query):
		if 'languagemodel' in query[ query_idx ]:
			query_lm = query[ query_idx]['languagemodel']
		else:
			query_lm = normalize(query[query_idx]['wordcount'], inplace=False)

		answer_set = query[query_idx]['answer']

		name_answer_set = {}
		for key, val in answer_set.items():
			docname = 'T' + str(key).zfill(4)
			name_answer_set[ docname ] = val

		ret = engine.retrieve(query_lm, negquery=None)

		# Calculate Mean Average Precision
		ap = evalAP(ret,name_answer_set)
		aps.append(ap)

	# Time end
	_end_time = time.time()
	print("Mean Average Precision: {}".format(np.mean(aps)))
	print("Time taken: {} seconds".format(_end_time - _start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--query_pickle',type=str,default='./queries/PTV.dnn.onebest.jieba.query.pickle')
	parser.add_argument('-d', '--data_dir', type=str, default='./iscr/searchengine/data/PTV.dnn.onebest.jieba')
	args = parser.parse_args()

	run_ap_baseline(args.query_pickle, args.data_dir)