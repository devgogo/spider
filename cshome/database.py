# -*- coding: utf-8 -*-

import pymysql.cursors
from cshome.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_CHARSET

connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset=MYSQL_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor)


def save_question(item):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `question` (`title`, `body`, `category`, `sub_category`,`source_name`," \
              " `source_url`, `entry_url`, `num_answers`, `created_at`)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())"
        cursor.execute(sql, (
            item.get('title'), item.get('body'), item.get('category'), item.get('sub_category'),
            item.get('source_name'), item.get('source_url'), item.get('entry_url'), len(item.get('answers'))))

        connection.commit()

        item['id'] = cursor.lastrowid

    for answer in item.get('answers'):
        with connection.cursor() as cursor:
            sql = "INSERT INTO `answer` (`question_id`, `body`) VALUES (%s, %s)"
            cursor.execute(sql, (item.get('id'), answer.get('body')))

        connection.commit()
        answer['id'] = cursor.lastrowid
