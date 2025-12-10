# Langflow Implementation

## Overview
We implemented the LLM workflow using Langflow cloud platform to demonstrate visual LLM chaining as required by the project specifications.

## Workflow Components

1. **Text Input** - Receives customer review text
2. **Prompt Template** - Formats analysis instructions
3. **Language Model (OpenAI)** - Processes and analyzes reviews
4. **Chat Output** - Displays structured results

## Test Results

**Input Review:** "The food was great but service was slow"

**AI Analysis Output:**
- **Sentiment:** Mixed (Positive for food, Negative for service)
- **Main Topics:** Food Quality, Service Speed  
- **Recommendation:** Investigate and address causes of slow service, potentially by optimizing staffing levels during peak hours or improving staff training on efficiency

## Screenshots

- Workflow Architecture: `docs/langflow_screenshots/langflow_workflow_full.png`
- Live Test Results: `docs/langflow_screenshots/langflow_playground_test.png`
- Configuration: `docs/langflow_screenshots/langflow_settings.png`

## Files
- Flow Export: `"C:\Users\kirut\Downloads\Sentiment Analysis.json"`

This implementation satisfies the project requirement to "Use Langflow to chain LLM components for sentiment classification, topic extraction, and summarized insights." 