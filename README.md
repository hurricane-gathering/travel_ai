`uvicorn app:app --host 0.0.0.0 --port 3040 --reload`

```bash
curl -X POST "http://localhost:3040/query" \
    -H "Content-Type: application/json" \
    --data '{"query": "推荐上海十大旅游景点"}'
```