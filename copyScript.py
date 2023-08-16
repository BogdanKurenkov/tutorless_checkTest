from __future__ import annotations
from dataclasses import dataclass
import json


TRANSFORM_POINTS = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 9,
    9: 10,
    10: 12,
    11: 14,
    12: 16,
    13: 18,
    14: 20,
    15: 22,
    16: 23,
    17: 25,
    18: 27,
    19: 28,
    20: 29,
    21: 31,
    22: 32,
    23: 34,
    24: 35,
    25: 36,
    26: 37,
    27: 38,
    28: 39,
    29: 41,
    30: 42,
    31: 43,
    32: 44,
    33: 45,
    34: 46,
    35: 47,
    36: 48,
    37: 49,
    38: 50,
    39: 51,
    40: 52,
    41: 53,
    42: 54,
    43: 55,
    44: 56,
    45: 57,
    46: 58,
    47: 59,
    48: 60,
    49: 61,
    50: 62,
    51: 63,
    52: 64,
    53: 65,
    54: 66,
    55: 67,
    56: 68,
    57: 69,
    58: 70,
    59: 71,
    60: 72,
    61: 73,
    62: 74,
    63: 75,
    64: 76,
    65: 77,
    66: 78,
    67: 79,
    68: 80,
    69: 81,
    70: 82,
    71: 83,
    72: 84,
    73: 85,
    74: 87,
    75: 89,
    76: 90,
    77: 92,
    78: 96,
    79: 98,
    80: 100
}

@dataclass
class Test:
    id: int
    userFullname: str
    date: str
    fullTime: int
    answers: list[Answer]

@dataclass
class DataFromServer:
    name: str
    subject: str
    timeCommentaries: str
    questions: list[Question]

@dataclass
class Question:
    id: int
    name: str
    type: str
    task: str
    addition: str | None
    image: str | None
    variants: list[Variant] | None
    letterRatioVariants: list[str] | None
    numericRatioVariants: list[str] | None
    commentary: str
    acceptableTime: int
    themesIndexes: list[str]

@dataclass
class Variant:
    id: int
    text: str | None
    accuracy: True | False
    themes: list[str] | None

@dataclass
class Answer:
    id: int
    time: int
    answers: list[str]

@dataclass
class Analytics:
    userFullname: Test.userFullname
    date: Test.date
    subject: DataFromServer.subject
    testName: DataFromServer.name
    primaryScore: int
    scorePercentage: int
    rightAnswersAmount: int
    themes: list[Theme]
    questions: list[AnalyticsQuestion]

@dataclass
class AnalyticsQuestion:
    id: Question.id
    name: Question.name
    type: Question.type
    task: Question.task
    addition: Question.addition | None
    image: Question.image | None
    variants: Question.variants | None
    letterRatioVariants: Question.letterRatioVariants | None
    numericRatioVariants: Question.numericRatioVariants | None
    userAnswer: Answer.answers | None
    time: int
    status: str
    commentary: Question.commentary

@dataclass
class AnalyticsVariants:
    id: Variant.id
    text: Variant.text
    accuracy: Variant.accuracy
    isChosen: True | False

@dataclass
class Theme:
    level: int
    text: str

def getNecessaryData(client, server):
    with open(client, encoding='utf-8') as f:
        data = json.load(f)
        answers: list(Answer) = []
        for answerObject in data['answers']:
            answers.append(Answer(
                id=answerObject['id'],
                time=answerObject['time'],
                answers=answerObject['answers']
            ))
        test = Test(
            id=data['id'],
            userFullname=data['userFullname'],
            date=data['date'],
            fullTime=data['fullTime'],
            answers=answers
        )

    with open(server, encoding='utf-8') as f:
        data = json.load(f)

    return test

def main(client, server):
    data = getNecessaryData(client, server)
    print(data)

main("client1.json", "server.json")
