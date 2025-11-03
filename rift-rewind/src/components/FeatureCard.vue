<template>
  <div class="feature-card" :style="cardStyle" @click="handleClick">
    <div class="card-background"></div>

    <div class="card-content">
      <div class="icon-wrapper">
        <span class="icon">{{ feature.icon }}</span>
      </div>

      <h3 class="card-title">{{ feature.title }}</h3>
      <p class="card-description">{{ feature.description }}</p>

      <div class="card-footer">
        <span class="cta-text">Explore →</span>
      </div>
    </div>

    <div class="card-overlay"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  feature: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

const cardStyle = computed(() => ({
  '--accent-color': props.feature.color
}))

const handleClick = () => {
  emit('click')
}
</script>

<style scoped>
.feature-card {
  position: relative;
  background: rgba(30, 35, 70, 0.6);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 28px 24px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  animation: cardEntrance 0.6s ease-out backwards;

  --accent-color: #1976d2;
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card:nth-child(1) { animation-delay: 0.1s; }
.feature-card:nth-child(2) { animation-delay: 0.15s; }
.feature-card:nth-child(3) { animation-delay: 0.2s; }
.feature-card:nth-child(4) { animation-delay: 0.25s; }
.feature-card:nth-child(5) { animation-delay: 0.3s; }
.feature-card:nth-child(6) { animation-delay: 0.35s; }
.feature-card:nth-child(7) { animation-delay: 0.4s; }
.feature-card:nth-child(8) { animation-delay: 0.45s; }

.card-background {
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, var(--accent-color) 0%, transparent 70%);
  opacity: 0.08;
  border-radius: 50%;
  transition: all 0.4s ease;
}

.feature-card:hover .card-background {
  opacity: 0.12;
  transform: scale(1.2);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(var(--accent-color), 0) 0%, rgba(var(--accent-color), 0.05) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
  border-radius: 16px;
}

.feature-card:hover .card-overlay {
  opacity: 1;
}

.card-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--accent-color) 0%, rgba(var(--accent-color), 0.8) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(var(--accent-color), 0.3);
  transition: all 0.4s ease;
}

.feature-card:hover .icon-wrapper {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 8px 25px rgba(var(--accent-color), 0.5);
}

.icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.feature-card:hover .card-title {
  color: var(--accent-color);
  filter: drop-shadow(0 0 8px rgba(var(--accent-color), 0.3));
}

.card-description {
  font-size: 14px;
  color: #b0bec5;
  margin: 0;
  line-height: 1.6;
  flex-grow: 1;
  transition: color 0.3s ease;
}

.feature-card:hover .card-description {
  color: #cfd8dc;
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.cta-text {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.feature-card:hover .cta-text {
  transform: translateX(4px);
  filter: drop-shadow(0 0 4px rgba(var(--accent-color), 0.5));
}

.feature-card:hover {
  border-color: rgba(var(--accent-color), 0.3);
  box-shadow:
    0 12px 40px rgba(var(--accent-color), 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transform: translateY(-8px);
}

.feature-card:active {
  transform: translateY(-4px);
}

@media (max-width: 768px) {
  .feature-card {
    padding: 24px 20px;
    min-height: 280px;
  }

  .card-title {
    font-size: 18px;
  }

  .card-description {
    font-size: 13px;
  }

  .icon-wrapper {
    width: 56px;
    height: 56px;
  }

  .icon {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .feature-card {
    padding: 20px 16px;
    min-height: 260px;
  }

  .card-background {
    width: 150px;
    height: 150px;
  }

  .icon-wrapper {
    width: 52px;
    height: 52px;
  }

  .icon {
    font-size: 24px;
  }

  .card-title {
    font-size: 16px;
  }

  .card-description {
    font-size: 12px;
  }
}
</style>
