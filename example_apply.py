# example_apply.py
import os
import pandas as pd
from nlp_utils import preprocess_text

# (예시) 기존 CSV나 DB에서 로드된 데이터프레임이라고 가정
# df = pd.read_sql("SELECT id, title, content FROM news", conn)
df = pd.DataFrame({
    "title": [
        "OpenAI launches new model in 2025!",
        "국내 AI 스타트업, 머신러닝 신기술 공개"
    ],
    "content": [
        "This is a test CONTENT with URLs like https://example.com and numbers 123.",
        "인공지능 기술이 빠르게 성장하고 있다. 새로운 모델이 공개됐다."
    ]
})

# ── 전처리 적용: 토큰 리스트와 클린 텍스트(공백으로 join) ─────────────────────
df["title_tokens"]   = df["title"].astype(str).apply(preprocess_text)
df["content_tokens"] = df["content"].astype(str).apply(preprocess_text)
df["title_clean"]    = df["title_tokens"].apply(lambda xs: " ".join(xs))
df["content_clean"]  = df["content_tokens"].apply(lambda xs: " ".join(xs))

# ── 저장 (예: .env의 DATA_DIR를 사용하고 싶으면 os.getenv로 경로 받기) ────────
out_dir = os.getenv("DATA_DIR", "/tmp")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "news_tokens.csv")
df.to_csv(out_path, index=False)
print(f"Saved → {out_path}")
