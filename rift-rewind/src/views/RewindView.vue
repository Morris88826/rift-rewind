<template>
  <div class="rewind-container">
    <div class="background-overlay"></div>

    <div class="content">
      <!-- Header -->
      <div class="header-section">
        <div class="header-content">
          <h1 class="main-title">Your Rift Rewind</h1>
          <p class="user-info">{{ riotId }} • {{ region }}</p>
        </div>
        <button class="back-btn" @click="goHome">← Back</button>
      </div>

      <!-- Features Grid -->
      <div class="features-grid">
        <FeatureCard
          v-for="feature in features"
          :key="feature.id"
          :feature="feature"
          @click="handleFeatureClick(feature.id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import FeatureCard from '@/components/FeatureCard.vue'

const router = useRouter()
const route = useRoute()

const riotId = computed(() => route.params.riotId || 'Unknown')
const region = computed(() => route.params.region || 'N/A')

const features = [
  {
    id: 'guesser',
    title: 'League Guesser',
    description: 'Test your knowledge with champion and game prediction challenges',
    icon: '🎯',
    color: '#ff6b6b'
  },
  {
    id: 'mastery',
    title: 'Mastery',
    description: 'Explore your champion mastery progression and achievements',
    icon: '👑',
    color: '#ffd93d'
  },
  {
    id: 'lp-progress',
    title: 'LP Progress',
    description: 'Track your ranked LP journey throughout the season',
    icon: '📈',
    color: '#6bcf7f'
  },
  {
    id: 'social',
    title: 'Social',
    description: 'Connect with friends and share your achievements',
    icon: '👥',
    color: '#4d96ff'
  },
  {
    id: 'calendar',
    title: 'Calendar',
    description: 'View your match history in a beautiful calendar layout',
    icon: '📅',
    color: '#a78bfa'
  },
  {
    id: 'fun-facts',
    title: 'Fun Facts',
    description: 'Discover interesting statistics and facts about your gameplay',
    icon: '✨',
    color: '#ff8fab'
  },
  {
    id: 'infographic',
    title: 'Infographic',
    description: 'Visual breakdown of your performance and play style',
    icon: '📊',
    color: '#5eb3d6'
  },
  {
    id: 'collection',
    title: 'Collection',
    description: 'Browse your skins, emotes, and cosmetic collection',
    icon: '💎',
    color: '#f5a962'
  }
]

const goHome = () => {
  router.push({ name: 'home' })
}

const handleFeatureClick = (featureId) => {
  if (featureId === 'calendar') {
    router.push({
      name: 'calendar',
      params: {
        riotId: riotId.value,
        region: region.value,
      },
    })
  } else if (featureId === 'infographic') {
    router.push({
      name: 'infographic',
      params: {
        riotId: riotId.value,
        region: region.value,
      },
    })
  } else if (featureId === 'mastery') {
    router.push({
      name: 'mastery',
      params: {
        riotId: riotId.value,
        region: region.value,
      },
    })
  } else if (featureId === 'guesser') {
    router.push({
      name: 'guesser',
      params: {
        riotId: riotId.value,
        region: region.value,
      },
    })
  } else {
    console.log(`Clicked on ${featureId}`)
    // TODO: Navigate to other feature pages
  }
}
</script>

<style scoped>
.rewind-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1628 100%);
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.15;
  z-index: 0;
}

.rewind-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(25, 118, 210, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(56, 142, 60, 0.05) 0%, transparent 50%);
  z-index: 0;
  pointer-events: none;
}

.content {
  position: relative;
  z-index: 1;
  padding: 60px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 60px;
  animation: slideDown 0.8s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content {
  flex: 1;
}

.main-title {
  font-size: 52px;
  font-weight: 800;
  color: #fff;
  margin: 0 0 12px 0;
  letter-spacing: -1.5px;
  background: linear-gradient(135deg, #ffffff 0%, #64b5f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-info {
  font-size: 18px;
  color: #90caf9;
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.back-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateX(-4px);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  animation: fadeIn 0.8s ease-out 0.2s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 1200px) {
  .content {
    padding: 40px 30px;
  }

  .main-title {
    font-size: 40px;
  }

  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .content {
    padding: 30px 20px;
  }

  .header-section {
    flex-direction: column;
    gap: 20px;
    margin-bottom: 40px;
  }

  .main-title {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .user-info {
    font-size: 16px;
  }

  .back-btn {
    align-self: flex-start;
  }

  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .content {
    padding: 20px 16px;
  }

  .main-title {
    font-size: 24px;
    margin-bottom: 6px;
  }

  .user-info {
    font-size: 14px;
  }

  .back-btn {
    padding: 10px 18px;
    font-size: 14px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
