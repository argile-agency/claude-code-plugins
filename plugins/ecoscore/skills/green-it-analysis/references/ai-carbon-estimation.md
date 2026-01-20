# AI/LLM Carbon Estimation Methodology

Estimate environmental impact of AI model usage in applications.

## Carbon Per Token Estimates

### By Model Size

| Model Category | Example Models | gCO2e per 1K tokens |
|----------------|----------------|---------------------|
| Small (< 10B params) | Claude Haiku, GPT-3.5, Gemini Flash | 0.1 - 0.3 |
| Medium (10-100B params) | Claude Sonnet, GPT-4-mini | 0.3 - 0.8 |
| Large (> 100B params) | Claude Opus, GPT-4, Gemini Ultra | 0.8 - 2.0 |

**Note:** Estimates vary based on:
- Provider infrastructure efficiency
- Data center location (carbon intensity)
- Model architecture and optimization
- Time of day (grid carbon varies)

### Calculation Formula

```
Total CO2e = (input_tokens + output_tokens) / 1000 × carbon_per_1k_tokens
```

For daily/monthly estimates:
```
Monthly CO2e = daily_requests × avg_tokens_per_request / 1000 × carbon_per_1k × 30
```

## Model Selection Guidelines

### When to Use Small Models

- Text classification
- Sentiment analysis
- Simple Q&A with known formats
- Summarization of short texts
- Entity extraction
- Language detection

**Carbon savings:** 70-90% vs large models

### When to Use Medium Models

- Code generation (simple)
- Content moderation
- Translation
- Structured data extraction
- Conversational AI (standard)

**Carbon savings:** 30-60% vs large models

### When Large Models Are Justified

- Complex reasoning tasks
- Multi-step problem solving
- Code review and complex generation
- Creative writing requiring nuance
- Tasks requiring broad knowledge synthesis

## Token Efficiency Patterns

### Prompt Optimization

**Verbose prompt (wasteful):**
```
I would like you to help me with the following task. Please take your time
and think carefully about this. I need you to summarize the following text
in a concise manner. The text is about environmental sustainability and I
would like the summary to capture the main points. Here is the text:
[content]
```

**Efficient prompt:**
```
Summarize the key points (3 bullets max):
[content]
```

**Savings:** ~60% fewer input tokens

### Response Control

**Wasteful:**
```
Please provide a detailed explanation with examples...
```

**Efficient:**
```
Reply in JSON format: {"answer": string, "confidence": number}
```

**Savings:** ~80% fewer output tokens

### Caching Strategies

**Cache opportunities:**

1. **System prompts** - Use prompt caching (Claude) or similar
2. **Static context** - Cache embeddings for RAG
3. **Repeated queries** - Cache responses for identical inputs
4. **User sessions** - Maintain conversation context efficiently

**Example cache check:**
```python
cache_key = hash(prompt + model_id)
if cache_key in response_cache:
    return response_cache[cache_key]  # Zero additional carbon
```

### Batch Processing

**Wasteful (serial):**
```python
for item in items:
    response = llm.complete(f"Classify: {item}")  # N API calls
```

**Efficient (batch):**
```python
batch_prompt = "Classify each:\n" + "\n".join(items)
responses = llm.complete(batch_prompt)  # 1 API call
```

**Savings:** ~50% fewer tokens (no repeated instructions)

## Code Pattern Detection

### Anti-Patterns to Flag

**Hardcoded large model:**
```python
# Flag this
client.messages.create(model="claude-opus-4-5-20251101", ...)
# Suggest: Consider claude-sonnet-4-20250514 for this task
```

**Missing caching:**
```python
# Flag: repeated identical calls
for user in users:
    greeting = llm.complete("Generate greeting")  # Same prompt!
```

**Verbose system prompts:**
```python
# Flag: system prompt > 500 tokens on every request
system = """You are a helpful assistant. You should always be polite and
considerate. When answering questions, please think step by step..."""
# Suggest: Use prompt caching or reduce system prompt
```

**No streaming when appropriate:**
```python
# Flag: long content generated but not streamed
response = llm.complete("Write a 2000 word essay...")  # User waits
# Suggest: Stream for better UX and allows early termination
```

### Recommended Patterns

**Model routing:**
```python
def select_model(task_complexity: str) -> str:
    models = {
        "simple": "claude-haiku",
        "medium": "claude-sonnet",
        "complex": "claude-opus"
    }
    return models.get(task_complexity, "claude-sonnet")
```

**Token budgeting:**
```python
def complete_with_budget(prompt: str, max_tokens: int = 500):
    """Enforce token limits to prevent runaway costs/carbon."""
    return client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=min(max_tokens, 1000),  # Hard cap
        messages=[{"role": "user", "content": prompt}]
    )
```

**Response caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_llm_call(prompt_hash: str, model: str) -> str:
    # Only called on cache miss
    return client.messages.create(...)
```

## Comparative Impact

### Perspective on AI Carbon

| Activity | CO2e |
|----------|------|
| 1 Google search | 0.2g |
| 1 email | 4g |
| 1 ChatGPT query (GPT-4) | 4-5g |
| 1 Claude Opus query (1K tokens) | 1-2g |
| 1 Claude Haiku query (1K tokens) | 0.1-0.3g |
| 1 km driving (avg car) | 120g |
| Streaming 1 hour video | 36g |

### Application-Level Impact

For an app with 1M daily AI requests:

| Scenario | Monthly CO2e |
|----------|--------------|
| All large models, no optimization | 60-150 tonnes |
| Smart model routing | 20-40 tonnes |
| + Caching (50% hit rate) | 10-20 tonnes |
| + Prompt optimization | 5-10 tonnes |

**Potential savings:** 80-95% with full optimization

## Scoring Rubric

### AI Usage Score (0-100)

| Score | Criteria |
|-------|----------|
| 90-100 | Model routing, caching, optimized prompts, budgets |
| 70-89 | Some optimization, appropriate model choices |
| 50-69 | Basic usage, room for optimization |
| 30-49 | Large models overused, no caching |
| 0-29 | No optimization, excessive API calls |

### Checklist Items

- [ ] Model selection matches task complexity
- [ ] Prompt caching enabled where available
- [ ] Response caching for repeated queries
- [ ] Token limits enforced
- [ ] Prompts optimized for brevity
- [ ] Batch processing where applicable
- [ ] Streaming for long responses
- [ ] Monitoring of token usage
