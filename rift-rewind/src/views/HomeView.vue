<template>
  <div class="home-container">
    <div class="background-overlay"></div>

    <div class="content-wrapper">
      <div class="card-container">
        <div class="logo-section">
          <!-- <img src="/league-logo.png" alt="Logo" class="logo-image" /> -->
        </div>

        <div class="text-section">
          <h1 class="main-title">It's Rift Rewind Time</h1>
          <p class="subtitle">Search up your Riot ID to get started!</p>
          <p class="description">Relive your best League of Legends moments</p>
        </div>

        <div class="search-section">
          <SearchBar @search="goToRewind" />
        </div>

        <div class="footer-text">
          <p class="hint">Type your Riot ID and we'll find your ranked history</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchBar from '@/components/SearchBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToRewind = (searchData) => {
  // Navigate to the rewind page with the Riot ID and region
  const { riotId, region } = searchData
  router.push({ name: 'rewind', params: { riotId, region } })
}
</script>

<style scoped>
.home-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
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
  opacity: 0.25;
  z-index: 0;
}

.home-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(25, 118, 210, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(56, 142, 60, 0.08) 0%, transparent 50%);
  z-index: 0;
  pointer-events: none;
}

.content-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 40px 20px;
}

.card-container {
  background: rgba(26, 31, 58, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px;
  padding: 80px 60px;
  width: 100%;
  max-width: 600px;
  box-shadow:
    0 8px 32px rgba(31, 38, 135, 0.2),
    inset 1px 1px 0 rgba(255, 255, 255, 0.08);
  animation: slideUp 0.8s ease-out, glow 3s ease-in-out infinite;
  position: relative;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow:
      0 8px 32px rgba(31, 38, 135, 0.2),
      inset 1px 1px 0 rgba(255, 255, 255, 0.08);
  }
  50% {
    box-shadow:
      0 8px 32px rgba(31, 38, 135, 0.3),
      inset 1px 1px 0 rgba(255, 255, 255, 0.12);
  }
}

.logo-section {
  margin-bottom: 50px;
  text-align: center;
}

.logo-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  filter: drop-shadow(0 0 15px rgba(25, 118, 210, 0.6));
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.text-section {
  text-align: center;
  margin-bottom: 50px;
}

.main-title {
  font-size: 48px;
  font-weight: 800;
  color: #fff;
  margin: 0 0 20px 0;
  letter-spacing: -1px;
  line-height: 1.1;
  background: linear-gradient(135deg, #ffffff 0%, #64b5f6 50%, #bbdefb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  word-spacing: 0.1em;
}

.subtitle {
  font-size: 20px;
  color: #90caf9;
  margin: 0 0 16px 0;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.description {
  font-size: 15px;
  color: #b0bec5;
  margin: 0;
  font-style: italic;
  font-weight: 300;
  opacity: 0.9;
}

.search-section {
  margin-bottom: 40px;
}

.footer-text {
  text-align: center;
  margin-top: 30px;
  animation: fadeIn 1s ease-out 0.4s both;
}

.hint {
  font-size: 13px;
  color: #80a0ac;
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .card-container {
    padding: 60px 40px;
    max-width: 100%;
    border-radius: 20px;
  }

  .main-title {
    font-size: 36px;
  }

  .subtitle {
    font-size: 18px;
  }

  .description {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 20px;
  }

  .card-container {
    padding: 40px 24px;
    border-radius: 16px;
  }

  .main-title {
    font-size: 28px;
    margin-bottom: 16px;
  }

  .subtitle {
    font-size: 16px;
    margin-bottom: 12px;
  }

  .description {
    font-size: 13px;
  }

  .text-section {
    margin-bottom: 40px;
  }

  .search-section {
    margin-bottom: 30px;
  }

  .footer-text {
    margin-top: 20px;
  }
}
</style>
