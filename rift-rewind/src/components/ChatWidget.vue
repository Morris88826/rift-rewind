<template>
  <!-- Floating Chat Button -->
  <button
    @click="toggleChat"
    class="chat-fab"
    aria-label="Open chat assistant"
    :class="{ active: isOpen }"
  >
    <svg
      v-if="!isOpen"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    <svg
      v-else
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>

  <!-- Chat Modal -->
  <Transition name="slide-up">
    <div v-if="isOpen" class="chat-modal">
      <div class="chat-header">
        <h3>AI Assistant</h3>
        <button @click="toggleChat" class="close-btn" aria-label="Close chat">×</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="message"
          :class="{ user: message.isUser, assistant: !message.isUser }"
        >
          <div class="message-content">
            {{ message.text }}
          </div>
          <span v-if="!message.isUser" class="message-time">{{ formatTime(message.timestamp) }}</span>
        </div>

        <!-- Typing indicator -->
        <div v-if="isLoading" class="message assistant typing">
          <div class="message-content">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          type="text"
          placeholder="Ask me anything..."
          class="chat-input"
          :disabled="isLoading"
        />
        <button
          @click="sendMessage"
          class="send-btn"
          :disabled="!userInput.trim() || isLoading"
          aria-label="Send message"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const isOpen = ref(false)
const isLoading = ref(false)
const userInput = ref('')
const messagesContainer = ref(null)
const messages = ref([
  {
    text: 'Hey there! I\'m your AI assistant. Ask me anything about League of Legends, gaming, or how to use Rift Rewind!',
    isUser: false,
    timestamp: new Date(),
  },
])

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const formatTime = (date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = async () => {
  const message = userInput.value.trim()
  if (!message) return

  // Add user message
  messages.value.push({
    text: message,
    isUser: true,
    timestamp: new Date(),
  })

  userInput.value = ''
  isLoading.value = true

  // Scroll to bottom
  await nextTick()
  scrollToBottom()

  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Get AI response (placeholder - integrate with actual API)
  const response = await getAIResponse(message)

  // Add assistant response
  messages.value.push({
    text: response,
    isUser: false,
    timestamp: new Date(),
  })

  isLoading.value = false

  // Scroll to bottom
  await nextTick()
  scrollToBottom()
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const getAIResponse = async (userMessage) => {
  // TODO: Replace this with actual API call
  // Example: OpenAI API, Claude API, or your own backend

  // Placeholder responses
  const placeholderResponses = [
    'That\'s a great question! I\'m currently a demo version. To integrate with a real AI, replace this function with an API call to your preferred AI service (like OpenAI, Claude, or your own backend).',
    'I\'m learning! Right now I can only provide placeholder responses, but once you integrate me with an AI API, I can give you real answers about League of Legends, gaming, and help you use Rift Rewind.',
    'Thanks for chatting with me! To make me fully functional, you\'ll need to integrate an AI service. Check the getAIResponse function in ChatWidget.vue for integration instructions.',
    'I\'m ready to help! Please integrate me with your preferred AI API to provide real, intelligent responses.',
  ]

  return placeholderResponses[Math.floor(Math.random() * placeholderResponses.length)]
}
</script>

<style scoped>
/* Floating Action Button */
.chat-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border: none;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 999;
  font-size: 24px;
}

.chat-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6);
}

.chat-fab:active {
  transform: scale(0.95);
}

.chat-fab.active {
  background: linear-gradient(135deg, #a855f7, #6366f1);
}

/* Chat Modal */
.chat-modal {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 380px;
  max-height: 600px;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 998;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #e2e8f0;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 28px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #e2e8f0;
}

/* Messages Container */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  animation: slideIn 0.3s ease-out;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-content {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.5;
}

.message.user .message-content {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: rgba(71, 85, 105, 0.5);
  color: #cbd5e1;
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.message-time {
  font-size: 12px;
  color: #64748b;
  padding: 0 4px;
}

/* Typing Indicator */
.typing .message-content {
  padding: 10px 16px;
  display: flex;
  gap: 6px;
  align-items: center;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  animation: bounce 1.4s infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    opacity: 0.5;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-10px);
  }
}

/* Input Area */
.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid rgba(99, 102, 241, 0.2);
  background: rgba(10, 14, 39, 0.5);
}

.chat-input {
  flex: 1;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  padding: 8px 12px;
  color: #e2e8f0;
  font-size: 14px;
  transition: all 0.2s;
}

.chat-input::placeholder {
  color: #64748b;
}

.chat-input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(30, 41, 59, 1);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.chat-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  color: white;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  box-shadow: 0 2px 12px rgba(99, 102, 241, 0.4);
}

.send-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Responsive Design */
@media (max-width: 480px) {
  .chat-modal {
    width: calc(100vw - 32px);
    max-height: 70vh;
    bottom: 100px;
    right: 16px;
  }

  .message-content {
    max-width: 90%;
    font-size: 13px;
  }
}

/* Scrollbar Styling */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.5);
}
</style>
