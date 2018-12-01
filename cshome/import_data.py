from cshome.database import *
from cshome.elastic import *
from cshome.utils import text_filter


class Process:

    def run(self, source_question):
        try:
            print('----------------------')
            print("Process question %d:\t%s" % (source_question['id'], source_question['title']))
            print(source_question)

            query = {
                "query": {
                    "bool": {
                        "must": {
                            "more_like_this": {
                                "fields": [
                                    "title",
                                    "body"
                                ],
                                "minimum_should_match": "70%",
                                "like_text": source_question['title'],
                                "min_term_freq": 1,
                                "min_word_len": 1
                            }
                        },
                        "must_not": [{
                            "term": {"id": source_question['id']}
                        }, {
                            "exists": {"field": "flag"}  # 未进行匹配的问题
                        }]
                    }

                },
                "size": 1
            }

            tags = ''

            if source_question['category']:
                tags = source_question['category']

            if source_question['category'] and source_question['sub_category']:
                tags = tags + ',' + source_question['sub_category']

            question_ids = [source_question['id']]
            question = {'title': source_question['title'], 'category': source_question['category'],
                        'sub_category': source_question['sub_category'], 'body': None,
                        'tags': tags}

            found_questions = search_question(query)

            if len(found_questions) < 1:
                print('******* Not found more like this docs')
                update_question(source_question['id'], {"script": 'ctx._source.flag = 2'})  # 没有匹配的答案
                return

            body_flag = False
            for q in found_questions:

                found_question = q['_source']
                question_ids.append(found_question['id'])

                if found_question['body'] and not body_flag:
                    question['body'] = found_question['body']
                    body_flag = True

                print('Found question %d:\t%s,%s' % (
                    found_question['id'], found_question['title'], found_question['body']))

            found_answers = find_answers_by_ids(question_ids)

            answer_texts = []
            answer_ids = []
            for answer in found_answers:
                answer_ids.append(answer['id'])
                answer_texts.append(answer['body'])

                answer_texts = list(set(answer_texts))

            answer_texts = filter(text_filter, answer_texts)

            answers = []
            for answer_txt in answer_texts:
                if len(answer_txt) < 5:
                    continue

                answers.append({
                    'body': answer_txt
                })

            question['num_answers'] = len(answers)
            question['answers'] = answers

            print('----------------------')
            print('question_ids', question_ids)
            print('answer_ids', answer_ids)
            print('Question', question)
            print('Answers')

            for answer in answers:
                print('-', answer)

            save_new_question(question)

            for qid in question_ids:
                update_question(qid, {"script": 'ctx._source.flag = 1'})  # 匹配过答案的问题

        except Exception as e:
            print('******* Error: ', e)

    def start(self):

        query = {
            "query": {
                "bool": {
                    "must_not": {
                        "exists": {"field": "flag"}
                    }
                }

            },
            "size": 100,
            "sort": {
                "id": "asc"
            }
        }

        while True:
            results = search_question(query)

            if len(results) == 0:
                print("******* Not found any questions")
                break

            for doc in results:
                question = doc['_source']
                print(question)

                self.run(question)


# reset_question_flag()

p = Process()
p.start()
