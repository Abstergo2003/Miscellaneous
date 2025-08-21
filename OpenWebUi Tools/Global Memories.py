"""
title: Global Memories, self growing knowledge database
author: Abstergo2003
author_url: https://github.com/Abstergo2003
funding_url: https://github.com/Abstergo2003
version: 0.5.0
"""

import os
from pydantic import BaseModel, Field
import psycopg2  # type: ignore
import spacy
import json
import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("MEMORY_DATABASE_URL")

nlp = spacy.load("pl_core_news_sm")


def get_keywords_polish(text: str):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]


def save_trivia_to_db(question: str, answer: str, user: str):
    conn = psycopg2.connect(DATABASE_URL)
    keywords = get_keywords_polish(question)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memory (question, answer, keywords, first_asked) VALUES (%s, %s, %s, %s);",
        (question, answer, json.dumps(keywords), user),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "success"}


def query_knowledge_table(sentence: str):
    keywords = get_keywords_polish(sentence)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
    SELECT * FROM (
        SELECT *, 
          (SELECT count(*) 
           FROM jsonb_array_elements_text(keywords) AS kw
           WHERE kw.value = ANY(%s::text[])) AS matches_count
        FROM memory
        WHERE keywords ?| %s::text[]
    ) AS sub
    WHERE matches_count >= 2
    ORDER BY matches_count DESC;
""",
        (keywords, keywords),
    )

    columns = [desc[0] for desc in cur.description]  # type: ignore

    # Fetch all rows
    rows = cur.fetchall()

    # Convert each row to dict with column names
    result_dicts = [dict(zip(columns, row)) for row in rows]

    # Convert list of dicts to JSON string
    def json_converter(o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        raise TypeError(f"Type {type(o)} not serializable")

    json_result = json.dumps(
        result_dicts, ensure_ascii=False, indent=2, default=json_converter
    )

    cur.close()
    conn.close()

    data = json.loads(json_result)

    if len(data):
        return f"""
        Answer to user question is {data[0]["answer"]}. Remember to return only relevant information. Do not change the answer.
        """
    else:
        return "Answer to this question is not in database. You must ask user if he wants to reroute his question to trusted human from same industry."


class Tools:
    def __init__(self):
        pass

    def get_answer_for_unchanging_fact(self, question: str) -> str:
        """
        If question has high probability of being about unchanging facts. Use this to get answer.
        :param question: Question asked by user.
        :return: Answer to question.
        """

        result = query_knowledge_table(question)

        return result

    def ask_human(self, __user__, question: str) -> str:
        """
        When users ask for it use this function to reroute his question to trusted human from same industry.
        :param question: Question asked by user.
        :return: Confirmation of rerouting
        """

        print(__user__["email"])

        return "Question was asked. Waiting time: max 1 day."
