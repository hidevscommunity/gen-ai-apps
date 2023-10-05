from sentence_transformers import SentenceTransformer, util
import json
import numpy as np
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def similarity(strQuery):

    inputs = json.load(open('chunks.json','r'))
    lstCorpus = [dct['text'] for dct in inputs]

    strQuery = "How many different document types?"
    qryEmbedding = model.encode(strQuery, convert_to_tensor=True)
    corpusEmbedding= model.encode(lstCorpus, convert_to_tensor=True)
        
    sim_mat = util.pytorch_cos_sim(qryEmbedding, corpusEmbedding)
    lstSim = sim_mat[0].tolist()
    npSim = np.array(lstSim)
    indexMax = npSim.argmax()
    scoreMax = npSim.max()

    return(inputs[indexMax]['start'], inputs[indexMax]['end'])

