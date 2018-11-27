# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

es = Elasticsearch()

question_index = 'question'
question_type = 'question'
answer_index = 'answer'
answer_type = 'answer'

question_mapping = '''{
    "mappings": {
        "question": {
            "properties": {
                "title": {
                    "type": "string",
                    "analyzer": "ik_smart"
                },
                "body": {
                    "type": "string",
                    "analyzer": "ik_smart"
                },
                "tags": {
                    "type": "keyword"
                }
            }
        }
    }
}'''

answer_mapping = '''{
    "mappings": {
        "answer": {
            "properties": {
                "body": {
                    "type": "string",
                    "analyzer": "ik_smart"
                }
            }
        }
    }
}'''


def create_index():
    if not es.indices.exists(index=question_index):
        es.indices.create(index=question_index, ignore=400, body=question_mapping)

    if not es.indices.exists(index=answer_index):
        es.indices.create(index=answer_index, ignore=400, body=answer_mapping)


def delete_index():
    es.indices.delete(index=question_index)
    es.indices.delete(index=answer_index)


def index_question(doc):
    es.index(index=question_index, doc_type=question_type, id=doc['id'], body=doc)


def index_answer(doc):
    es.index(index=answer_index, doc_type=answer_type, id=doc['id'], body=doc)


# delete_index()
# create_index()
