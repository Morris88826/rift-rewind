# Chatbot AI Integration Guide

The chatbot widget is now integrated into your Rift Rewind application! Currently, it shows placeholder responses, but you can easily integrate it with real AI services.

## Available Chatbot Features

- **Floating Chat Widget**: Fixed position floating button in bottom-right corner
- **Chat Modal**: Opens with smooth animations when clicked
- **Message History**: Displays all messages in a scrollable window
- **Typing Indicator**: Shows when the AI is processing
- **Responsive Design**: Works on mobile and desktop
- **Dark Theme**: Matches the Rift Rewind glassmorphism aesthetic

## Integration Options

### 1. OpenAI GPT API (Recommended for Production)

#### Setup:
1. Install the OpenAI library:
```bash
npm install openai
```

2. Update `src/components/ChatWidget.vue` - Replace the `getAIResponse` function:

```javascript
import { OpenAI } from 'openai'

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true // Only for development/testing
})

const getAIResponse = async (userMessage) => {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant for Rift Rewind, a League of Legends statistics application. Help users with questions about the app and League of Legends gaming.'
        },
        {
          role: 'user',
          content: userMessage
        }
      ],
      temperature: 0.7,
      max_tokens: 500
    })

    return response.choices[0].message.content
  } catch (error) {
    console.error('Error calling OpenAI API:', error)
    return 'Sorry, I encountered an error. Please try again.'
  }
}
```

3. Create a `.env.local` file:
```
VITE_OPENAI_API_KEY=your-api-key-here
```

4. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

---

### 2. Anthropic Claude API

#### Setup:
1. Install the Anthropic SDK:
```bash
npm install @anthropic-ai/sdk
```

2. Update the `getAIResponse` function in `ChatWidget.vue`:

```javascript
import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({
  apiKey: import.meta.env.VITE_CLAUDE_API_KEY,
  dangerouslyAllowBrowser: true // Only for development
})

const getAIResponse = async (userMessage) => {
  try {
    const response = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      system: 'You are a helpful assistant for Rift Rewind, a League of Legends statistics application. Help users with questions about the app and League of Legends gaming.',
      messages: [
        {
          role: 'user',
          content: userMessage
        }
      ]
    })

    return response.content[0].type === 'text' ? response.content[0].text : 'Unable to process response'
  } catch (error) {
    console.error('Error calling Claude API:', error)
    return 'Sorry, I encountered an error. Please try again.'
  }
}
```

3. Create a `.env.local` file:
```
VITE_CLAUDE_API_KEY=your-api-key-here
```

4. Get your API key from [Anthropic Console](https://console.anthropic.com/)

---

### 3. Custom Backend (Recommended for Production)

For security reasons, don't expose API keys in the browser. Instead, create a backend endpoint:

#### Backend Endpoint (Node.js/Express example):
```javascript
app.post('/api/chat', async (req, res) => {
  const { message } = req.body

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant for Rift Rewind, a League of Legends statistics application.'
        },
        {
          role: 'user',
          content: message
        }
      ]
    })

    res.json({ reply: response.choices[0].message.content })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})
```

#### Frontend Update in `ChatWidget.vue`:
```javascript
const getAIResponse = async (userMessage) => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    })

    const data = await response.json()
    return data.reply || 'Unable to process your message'
  } catch (error) {
    console.error('Error communicating with backend:', error)
    return 'Sorry, I encountered an error. Please try again.'
  }
}
```

---

### 4. Hugging Face Inference API

#### Setup:
1. Create a Hugging Face account and get an API key
2. Update the `getAIResponse` function:

```javascript
const getAIResponse = async (userMessage) => {
  try {
    const response = await fetch(
      'https://api-inference.huggingface.co/models/gpt2',
      {
        headers: { Authorization: `Bearer ${import.meta.env.VITE_HF_API_KEY}` },
        method: 'POST',
        body: JSON.stringify({ inputs: userMessage }),
      }
    )

    const result = await response.json()
    return result[0]?.generated_text || 'Unable to process your message'
  } catch (error) {
    console.error('Error calling Hugging Face API:', error)
    return 'Sorry, I encountered an error. Please try again.'
  }
}
```

---

## Configuration Tips

### Using Environment Variables
1. Create a `.env.local` file in the project root
2. Add your API keys:
   ```
   VITE_OPENAI_API_KEY=sk-...
   VITE_CLAUDE_API_KEY=sk-ant-...
   ```
3. Access in components with `import.meta.env.VITE_YOUR_KEY`

### System Prompt Customization
To tailor the chatbot's personality, modify the system prompt in the `getAIResponse` function:

```javascript
system: 'You are a friendly League of Legends expert helping players analyze their statistics on Rift Rewind. Be helpful, concise, and gaming-focused.'
```

### Conversation History
To maintain conversation context across messages, store the full message history:

```javascript
const conversationHistory = ref([
  {
    role: 'system',
    content: 'You are a helpful Rift Rewind assistant'
  }
])

const getAIResponse = async (userMessage) => {
  conversationHistory.value.push({
    role: 'user',
    content: userMessage
  })

  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: conversationHistory.value
  })

  const assistantMessage = response.choices[0].message.content
  conversationHistory.value.push({
    role: 'assistant',
    content: assistantMessage
  })

  return assistantMessage
}
```

---

## Security Best Practices

⚠️ **Important Security Notes:**

1. **Never commit API keys** to version control
2. **Always use environment variables** for sensitive data
3. **Use a backend server** to handle API calls in production
4. **Enable CORS properly** if calling external APIs from the browser
5. **Rate limit API calls** to prevent abuse
6. **Validate user input** before sending to AI services

---

## Styling Customization

The chatbot widget includes glassmorphism styling that matches Rift Rewind. To customize:

- **Colors**: Update the gradient in `.chat-fab` and `.send-btn`
- **Size**: Modify `width: 380px` in `.chat-modal`
- **Position**: Change `bottom: 100px; right: 24px;` in `.chat-modal`
- **Backdrop Blur**: Adjust `backdrop-filter: blur(10px)` value

---

## Troubleshooting

### Widget not appearing?
- Check that `ChatWidget` is imported in `App.vue`
- Verify z-index values don't conflict with other fixed elements
- Check browser console for errors

### Messages not sending?
- Verify API key is correctly set in environment variables
- Check network requests in browser DevTools
- Ensure error handling is working

### Styling issues?
- Clear browser cache (Ctrl+Shift+Delete)
- Check for CSS conflicts with Bootstrap
- Verify responsive breakpoints work on mobile

---

## Next Steps

1. Choose your preferred AI service
2. Install required packages
3. Replace the `getAIResponse` function
4. Add your API key to `.env.local`
5. Test the chatbot functionality
6. Deploy with proper environment variables

Happy chatting! 🚀
