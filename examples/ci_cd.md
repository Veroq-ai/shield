# Shield in CI/CD

Verify AI-generated content before it reaches production.

## GitHub Action

```yaml
name: Shield Check
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: veroq/shield-action@v1
        with:
          api-key: ${{ secrets.VEROQ_API_KEY }}
          prompts: tests/prompts.json
          threshold: 0.7
```

## CLI

```bash
npm install -g @veroq/cli

# Test a prompt suite
veroq test prompts.json --threshold 0.7

# Shield a single text
veroq shield "NVIDIA reported $22B in Q4 revenue"

# Pipe from stdin
echo "Some AI output" | veroq shield --source gpt-4o
```

## prompts.json format

```json
[
  {
    "prompt": "What was NVIDIA's Q4 2024 revenue?",
    "expected_facts": ["$22.1 billion"],
    "min_trust": 0.7
  },
  {
    "prompt": "Who is the CEO of Apple?",
    "expected_facts": ["Tim Cook"],
    "min_trust": 0.8
  }
]
```
