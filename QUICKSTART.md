# ADAM-ZERO Quick Start Guide

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get API keys:**
   - **Gemini API**: https://makersuite.google.com/app/apikey (free tier available)
   - **OpenAI API**: https://platform.openai.com/api-keys (optional, for ChatGPT review)

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your keys
```

## Quick Start

### 1. Test Fragment IR (No API keys needed)

```bash
# See the 8 core fragments
python fragment_spec.py

# Run full demo
python demo.py

# Run test suite
python tests/test_harness.py
```

### 2. Test Gemini Integration (Requires API key)

```bash
# Set your API key in .env first
python gemini_fragment_integration.py
```

### 3. Run Full ADAM-ZERO System

```bash
# Set API keys in .env first
python adam_zero.py
```

## Getting API Keys

**Gemini API (Required for orchestration):**
- Visit: https://makersuite.google.com/app/apikey
- Sign in with Google account
- Click "Get API key"
- Copy and paste into .env file

**OpenAI API (Optional - for ChatGPT review):**
- Visit: https://platform.openai.com/api-keys
- Create new API key
- Add to .env file

**Anthropic API (Optional - for future enhancements):**
- Visit: https://console.anthropic.com/
- Generate API key

## Quick Start Without API Keys

You can still explore Fragment IR without API keys:

```bash
# Run the Fragment IR demo (no API keys needed)
python demo.py

# Run the test harness
python tests/test_harness.py

# View fragment examples
python fragment_spec.py
```