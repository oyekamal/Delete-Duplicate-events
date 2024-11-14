-- Description: This query is used to find the most active users in the last 1 month and delete the duplicates for a specific user_id
SELECT user_id, COUNT(*) AS activity_count
FROM public.analytics_analyticsevent
WHERE sent_at >= NOW() - INTERVAL '1 month'  -- Filter for the last 1 month
GROUP BY user_id
ORDER BY activity_count DESC;  -- Sort by activity count (most active users first)


-- delete the duplicates
WITH duplicate_rows AS (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY user_id, sent_at ORDER BY id) AS rn
        FROM public.analytics_analyticsevent
        where user_id = 3781
			AND sent_at >= NOW() - INTERVAL '1 month'
    ) AS ranked
    WHERE rn > 1
)
DELETE FROM public.analytics_analyticsevent
WHERE id IN (SELECT id FROM duplicate_rows);

-- varify the duplicates are deleted
SELECT sent_at AS sent_at_truncated, COUNT(*) AS count
FROM public.analytics_analyticsevent
WHERE user_id = 3781
  AND  sent_at >= NOW() - INTERVAL '1 month'
GROUP BY sent_at;

--  varify the duplicates are deleted
SELECT *
FROM public.analytics_analyticsevent
WHERE user_id = 2372
  AND name LIKE 'lessonLesson%'  -- Using LIKE with % to match names starting with 'lessonLesson'
  AND sent_at >= NOW() - INTERVAL '1 month'
ORDER BY sent_at;