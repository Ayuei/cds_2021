import threading
import sys
sys.path.append("/home/vin/Projects/nir/")

from nir.interfaces.indexer import SemanticElasticsearchIndexer
from nir.interfaces.config import GenericConfig, ElasticsearchConfig
from nir.rankers.transformer_sent_encoder import Encoder

from queue import Queue
from tqdm import tqdm
from elasticsearch import helpers, Elasticsearch

BUF_SIZE = 1000
N_THREADS = 6


class ProducerThread(threading.Thread):
    def __init__(self, client, index, queue: Queue):
        super().__init__()
        self.client = client
        self.index = index
        self.q = queue

    def run(self):
        for document in tqdm(helpers.scan(self.client, index=self.index), total=360_000):
            q.put(document)

        return


if __name__ == "__main__":
    q = Queue(BUF_SIZE)

    config = GenericConfig.from_toml(
        fp="/home/vin/Projects/nir/configs/trec2022/embeddings.toml",
        field_class=GenericConfig
    )

    config.encoder = None
    es_config = ElasticsearchConfig.from_toml("./configs/elasticsearch.toml",
                                              field_class=ElasticsearchConfig)

    es_client = Elasticsearch(f"{es_config.protocol}://{es_config.ip}:{es_config.port}",
                              timeout=es_config.timeout)
    es_client_thread = Elasticsearch(f"{es_config.protocol}://{es_config.ip}:{es_config.port}",
                                     timeout=es_config.timeout)

    p = ProducerThread(es_client,
                       index=config.index,
                       queue=q)

    p.start()

    for _ in range(N_THREADS):
        indexer_t = SemanticElasticsearchIndexer(es_client_thread,
                                                 encoder=Encoder("/home/vin/Projects/nir/outputs/submission/trec_model/"),
                                                 index=config.index,
                                                 fields_to_encode=['BriefTitle', 'BriefSummary',
                                                                   'DetailedDescription'],
                                                 queue=q)

        indexer_t.start()
