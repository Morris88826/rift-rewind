<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="story-container" @click.stop>
      <!-- Header -->
      <div class="story-header">
        <div class="header-date">
          <h2>{{ formatDate }}</h2>
          <p>{{ matchCount }} {{ matchCount === 1 ? 'match' : 'matches' }}</p>
        </div>
        <button @click="$emit('close')" class="close-btn" aria-label="Close">×</button>
      </div>

      <!-- Progress Bar -->
      <div class="progress-container">
        <div v-for="(match, index) in matches" :key="index" class="progress-bar" :class="{ active: currentIndex === index }">
          <div class="progress-fill" :style="{ width: progressWidth }"></div>
        </div>
      </div>

      <!-- Story Content -->
      <div class="story-content">
        <Transition name="card-fade" mode="out-in">
          <div v-if="currentMatch" :key="currentIndex" class="match-card" :class="{ victory: currentMatch.result === 'Victory', defeat: currentMatch.result === 'Defeat' }">
          <!-- Champion Section -->
          <div class="champion-section">
            <div class="champion-circle" :class="currentMatch.champion.toLowerCase()">
              <span class="champion-icon">{{ currentMatch.champion[0] }}</span>
            </div>
            <div class="champion-info">
              <h3>{{ currentMatch.champion }}</h3>
              <p class="role">{{ currentMatch.role }}</p>
            </div>
            <div class="result-badge" :class="currentMatch.result.toLowerCase()">
              {{ currentMatch.result }}
            </div>
          </div>

          <!-- Stats Grid -->
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-label">K/D/A</div>
              <div class="stat-value">{{ currentMatch.kills }}/{{ currentMatch.deaths }}/{{ currentMatch.assists }}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">CS</div>
              <div class="stat-value">{{ currentMatch.cs }}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Duration</div>
              <div class="stat-value">{{ currentMatch.duration }}</div>
            </div>
            <div class="stat-box" :class="currentMatch.lp.includes('-') ? 'loss' : 'gain'">
              <div class="stat-label">LP</div>
              <div class="stat-value">{{ currentMatch.lp }}</div>
            </div>
          </div>

          <!-- KDA Stats -->
          <div class="kda-breakdown">
            <div class="kda-item kills">
              <span class="label">Kills</span>
              <span class="value">{{ currentMatch.kills }}</span>
            </div>
            <div class="kda-item deaths">
              <span class="label">Deaths</span>
              <span class="value">{{ currentMatch.deaths }}</span>
            </div>
            <div class="kda-item assists">
              <span class="label">Assists</span>
              <span class="value">{{ currentMatch.assists }}</span>
            </div>
          </div>

          <!-- Additional Info -->
          <div class="match-details">
            <div class="detail-item">
              <span class="detail-icon">⏱️</span>
              <span>Match Duration: {{ currentMatch.duration }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-icon">📊</span>
              <span>CS Score: {{ currentMatch.cs }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-icon">🎮</span>
              <span>Role: {{ currentMatch.role }}</span>
            </div>
          </div>

          <!-- Time -->
          <div class="match-time">{{ formatTime(currentMatch.timestamp) }}</div>
        </div>
        </Transition>
      </div>

      <!-- Navigation -->
      <div class="story-navigation">
        <button
          @click="previousMatch"
          class="nav-button prev"
          :disabled="currentIndex === 0"
          aria-label="Previous match"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <div class="match-counter">{{ currentIndex + 1 }} / {{ matchCount }}</div>

        <button
          @click="nextMatch"
          class="nav-button next"
          :disabled="currentIndex === matchCount - 1"
          aria-label="Next match"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>

      <!-- Swipe Hint -->
      <div class="swipe-hint">Swipe to navigate</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  day: Number,
  month: Number,
  year: Number,
  matches: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['close'])

const currentIndex = ref(0)

const currentMatch = computed(() => props.matches[currentIndex.value])

const matchCount = computed(() => props.matches.length)

const formatDate = computed(() => {
  const date = new Date(props.year, props.month - 1, props.day)
  return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })
})

const progressWidth = computed(() => {
  if (currentIndex.value === 0 || currentIndex.value === matchCount.value - 1) return '100%'
  return '100%'
})

const nextMatch = () => {
  if (currentIndex.value < matchCount.value - 1) {
    currentIndex.value++
  }
}

const previousMatch = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.story-container {
  width: 100%;
  max-width: 500px;
  height: 100vh;
  max-height: 800px;
  background: linear-gradient(135deg, #0a0e27, #1a1f3a);
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
  position: relative;
}

/* Header */
.story-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.header-date h2 {
  margin: 0;
  color: #e2e8f0;
  font-size: 1.3rem;
}

.header-date p {
  margin: 4px 0 0 0;
  color: #94a3b8;
  font-size: 0.875rem;
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

/* Progress Bar */
.progress-container {
  display: flex;
  gap: 4px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.2);
}

.progress-bar {
  flex: 1;
  height: 3px;
  background: rgba(148, 163, 184, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar.active {
  background: rgba(168, 85, 247, 0.5);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #a855f7);
  animation: progress 3s ease-out forwards;
}

@keyframes progress {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

/* Story Content */
.story-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-card {
  width: 100%;
  padding: 24px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
}

.match-card.victory {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(20, 48, 30, 0.6);
}

.match-card.defeat {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(48, 20, 20, 0.6);
}

/* Card Transition */
.card-fade-enter-active,
.card-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.card-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.card-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Champion Section */
.champion-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.champion-circle {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.champion-circle.ahri {
  background: linear-gradient(135deg, #c084fc, #d8b4fe);
}

.champion-circle.lux {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.champion-circle.zed {
  background: linear-gradient(135deg, #374151, #1f2937);
}

.champion-info {
  flex: 1;
}

.champion-info h3 {
  margin: 0 0 4px 0;
  color: #e2e8f0;
  font-size: 1.3rem;
}

.role {
  margin: 0;
  color: #94a3b8;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.result-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.result-badge.victory {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

.result-badge.defeat {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat-box {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}

.stat-box.loss {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}

.stat-box.gain {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.05);
}

.stat-label {
  color: #94a3b8;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.stat-value {
  color: #e2e8f0;
  font-size: 1.4rem;
  font-weight: 700;
}

.stat-box.loss .stat-value {
  color: #fca5a5;
}

.stat-box.gain .stat-value {
  color: #86efac;
}

/* KDA Breakdown */
.kda-breakdown {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.kda-item {
  flex: 1;
  text-align: center;
}

.kda-item.kills {
  color: #fca5a5;
}

.kda-item.deaths {
  color: #fca5a5;
}

.kda-item.assists {
  color: #86efac;
}

.kda-item .label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #94a3b8;
  margin-bottom: 4px;
  letter-spacing: 0.5px;
}

.kda-item .value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
}

/* Match Details */
.match-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #cbd5e1;
  font-size: 0.9rem;
}

.detail-icon {
  font-size: 1.2rem;
}

/* Match Time */
.match-time {
  text-align: center;
  color: #64748b;
  font-size: 0.8rem;
  margin-top: 16px;
}

/* Navigation */
.story-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(99, 102, 241, 0.2);
}

.nav-button {
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #e2e8f0;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-button:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.4);
  border-color: rgba(99, 102, 241, 0.6);
}

.nav-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.nav-button:active:not(:disabled) {
  transform: scale(0.95);
}

.match-counter {
  color: #cbd5e1;
  font-size: 0.9rem;
  font-weight: 600;
}

/* Swipe Hint */
.swipe-hint {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  color: #64748b;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  animation: fadeInOut 3s ease-in-out infinite;
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 600px) {
  .story-container {
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
  }

  .match-card {
    padding: 16px;
  }

  .champion-circle {
    width: 70px;
    height: 70px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .match-counter {
    font-size: 0.8rem;
  }
}
</style>
