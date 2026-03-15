from enum import Enum


class PolicyVerdict(str, Enum):
    CONSULTATION = 'CONSULTATION'
    BORDERLINE = 'BORDERLINE'
    PROHIBITED = 'PROHIBITED'


PROHIBITED_PATTERNS = [
    'напиши диссертацию',
    'напиши главу целиком',
    'сделай готовую статью',
    'обойди антиплагиат',
    'перепиши для антиплагиата',
    'write dissertation chapter',
    'write full article',
    'bypass plagiarism',
]


BORDERLINE_PATTERNS = [
    'готовый текст',
    'полностью напиши',
    'finish the article',
]


def classify_request(text: str) -> PolicyVerdict:
    normalized = text.lower()
    if any(item in normalized for item in PROHIBITED_PATTERNS):
        return PolicyVerdict.PROHIBITED
    if any(item in normalized for item in BORDERLINE_PATTERNS):
        return PolicyVerdict.BORDERLINE
    return PolicyVerdict.CONSULTATION
