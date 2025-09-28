# SQL 분석 결과

본 문서는 뉴스 파이프라인에서 적재된 데이터를 기반으로 작성한 SQL 분석 쿼리와 설명을 정리합니다.  
실행 결과는 캡쳐 이미지로만 확인 가능하며, SQL 자체와 분석 의도를 중심으로 기록합니다.

---

## 1) 최신 기사 샘플

```sql
SELECT title, published_at
FROM news
ORDER BY published_at DESC
LIMIT 5;

## 2) 단어빈도 분석 (최근 7일)
SELECT word, COUNT(*) AS freq
FROM (
    SELECT unnest(string_to_array(lower(title), ' ')) AS word
    FROM news
    WHERE published_at >= now() - interval '7 days'
) t
WHERE length(word) > 2
GROUP BY word
ORDER BY freq DESC
LIMIT 20;

## 3) 일별 집꼐 및 키워드 비율
SELECT 
    stat_date,
    article_count,
    ai_count,
    ml_count,
    ko_ai_count,
    ROUND(ai_count::decimal / NULLIF(article_count,0), 3) AS ai_ratio,
    ROUND(ml_count::decimal / NULLIF(article_count,0), 3) AS ml_ratio,
    ROUND(ko_ai_count::decimal / NULLIF(article_count,0), 3) AS ko_ai_ratio
FROM news_daily_stats
ORDER BY stat_date DESC
LIMIT 10;

