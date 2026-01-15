client<llm> DefaultOpenAI {
  provider "openai"
  options {
    model "gpt-4.1" // Default model
    api_key env.OPENAI_API_KEY
  }
}

// You can add more clients here, for example:
// client<llm> AnthropicClaude {
//   provider "anthropic"
//   options {
//     model "claude-3-opus-20240229"
//     api_key env.ANTHROPIC_API_KEY
//   }
// }
