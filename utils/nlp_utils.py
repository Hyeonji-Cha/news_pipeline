# nlp_utils.py
import os
import re

# ── 1) 영어/한국어 불용어 (가벼운 기본셋) ─────────────────────────────────────
EN_STOPWORDS = {
    "a","an","the","and","or","but","if","then","else","when","while","of","at","by",
    "for","with","about","against","between","into","through","during","before","after",
    "above","below","to","from","up","down","in","out","on","off","over","under",
    "again","further","once","here","there","all","any","both","each","few","more",
    "most","other","some","such","no","nor","not","only","own","same","so","than",
    "too","very","can","will","just","don","should","now","is","am","are","was","were",
}

KO_STOPWORDS = {
    "이","그","저","것","수","등","들","및","에서","으로","에게","으로써","부터","까지",
    "와","과","도","만","은","는","이랑","랑","으로서","대한","관련","합니다","한다",
    "했다","하며","하고","이다","있다","없다","위해","또한","그러나","하지만","그리고",
}

# ── 2) 불용어 확장: 로컬 파일로 추가하고 싶을 때(선택) ─────────────────────
def load_extra_stopwords(path: str) -> set:
    s = set()
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            s = {line.strip() for line in f if line.strip()}
    return s

# ── 3) 기본 토크나이저: 영문/숫자/한글 토큰을 분리 ─────────────────────────────
TOKEN_PATTERN = re.compile(r"[a-z0-9]+|[가-힣]+")  # 영문/숫자 or 한글 블록

def tokenize_basic(text: str) -> list:
    """소문자 변환 → 정규식 토큰화 (영문/숫자/한글)"""
    if not text:
        return []
    text = text.lower()                     # 소문자 변환 (한글엔 영향 없음)
    tokens = TOKEN_PATTERN.findall(text)    # 정규식으로 토큰 뽑기
    return tokens

# ── 4) 불용어 제거 + 길이 필터 ────────────────────────────────────────────────
def remove_stopwords(tokens: list,
                     extra_en_path: str = "",
                     extra_ko_path: str = "",
                     min_len: int = 2) -> list:
    """언어 구분 없이 공용으로 필터링: 영어/한국어 기본셋 + 사용자 추가셋"""
    en_extra = load_extra_stopwords(extra_en_path)
    ko_extra = load_extra_stopwords(extra_ko_path)

    en_sw = EN_STOPWORDS | en_extra
    ko_sw = KO_STOPWORDS | ko_extra

    cleaned = []
    for t in tokens:
        if len(t) < min_len:        # 1글자 토큰 제거(“a”, “이” 등)
            continue
        # 한글 토큰인지 간단 판별
        if re.fullmatch(r"[가-힣]+", t):
            if t in ko_sw:
                continue
        else:
            if t in en_sw:
                continue
        cleaned.append(t)
    return cleaned

# ── 5) 통합 전처리 함수 ───────────────────────────────────────────────────────
def preprocess_text(text: str,
                    extra_en_path: str = "",
                    extra_ko_path: str = "",
                    min_len: int = 2) -> list:
    """소문자 → 토큰화 → 불용어 제거까지 한 번에"""
    tokens = tokenize_basic(text)
    tokens = remove_stopwords(tokens,
                              extra_en_path=extra_en_path,
                              extra_ko_path=extra_ko_path,
                              min_len=min_len)
    return tokens
