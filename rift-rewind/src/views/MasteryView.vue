<template>
  <div class="mastery-container">
    <div class="mastery-header">
      <div class="header-top">
        <button @click="goBack" class="back-btn">← Back</button>
        <h1>Champion Mastery</h1>
        <div class="spacer"></div>
      </div>
      <p class="subtitle">Track your mastery progression and champion achievements</p>
    </div>

    <!-- Mastery Stats Summary -->
    <div class="mastery-stats">
      <div class="stat-card">
        <div class="stat-label">Champions Mastered</div>
        <div class="stat-value">{{ masteredChampions.length }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Mastery Points</div>
        <div class="stat-value">{{ totalMasteryPoints }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Avg Mastery Level</div>
        <div class="stat-value">{{ avgMasteryLevel }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Top Champion</div>
        <div class="stat-value">{{ topChampion }}</div>
      </div>
    </div>

    <!-- Champion Selection -->
    <div class="champion-selection">
      <h2>Track Champions</h2>
      <p class="selection-subtitle">Select champions to track their progression</p>
      <div class="champion-selector">
        <label v-for="champion in masteryData" :key="champion.name" class="champion-checkbox">
          <input
            type="checkbox"
            :value="champion.name"
            v-model="selectedChampions"
            class="checkbox-input"
          />
          <span class="checkbox-label">
            {{ champion.emoji }} {{ champion.name }}
            <span class="level-info">Lv {{ champion.level }}</span>
          </span>
        </label>
      </div>
      <div class="selection-actions">
        <button @click="selectAllChampions" class="action-btn">Select All</button>
        <button @click="clearSelection" class="action-btn secondary">Clear</button>
      </div>
    </div>

    <!-- Mastery Progression Chart -->
    <div class="progression-container" v-if="selectedChampions.length > 0">
      <h2>Mastery Progression Over Time</h2>
      <p class="chart-subtitle">{{ selectedChampions.length }} champion(s) selected</p>
      <div class="chart-holder">
        <canvas ref="progressionChart"></canvas>
      </div>
    </div>

    <div v-else class="no-selection">
      <p>👈 Select champions above to view their progression</p>
    </div>

    <!-- Single Champion Details (Only when one champion selected) -->
    <div class="champions-section" v-if="selectedChampions.length === 1">
      <h2>{{ selectedChampions[0] }} Details</h2>
      <div class="champions-grid">
        <div v-for="champion in topChampionsCards" :key="champion.name" class="player-card" :class="`rarity-${champion.rarity}`">
          <!-- Card Background -->
          <div class="card-background"></div>

          <!-- Champion Info -->
          <div class="card-content">
            <div class="card-header">
              <div class="avatar-section">
                <div class="avatar">{{ champion.emoji }}</div>
                <div class="level-indicator">{{ champion.level }}</div>
              </div>
              <div class="name-section">
                <h3 class="champion-name">{{ champion.name }}</h3>
                <p class="rarity-name">{{ champion.rarityName }}</p>
              </div>
            </div>

            <!-- Stats Row -->
            <div class="stats-row">
              <div class="stat">
                <span class="stat-label">Kills</span>
                <span class="stat-value">{{ champion.totalKills }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">Assists</span>
                <span class="stat-value">{{ champion.totalAssists }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">K/A Ratio</span>
                <span class="stat-value">{{ champion.kaRatio }}</span>
              </div>
            </div>

            <!-- Badges with Progression (Grid Layout) -->
            <div class="badges-container">
              <div v-for="badge in champion.badges" :key="badge.name" class="achievement-badge-wrapper" :class="{ achieved: badge.progress > 0 }">
                <div class="achievement-badge" :class="`badge-${badge.tier}`" :title="`${badge.description} - ${badge.requirement}`">
                  <span class="badge-icon">{{ badge.icon }}</span>
                  <span class="badge-tier">{{ badge.tier[0].toUpperCase() }}</span>
                </div>
                <div class="badge-info">
                  <div class="badge-progress-bar">
                    <div class="badge-progress-fill" :style="{ width: badge.progress + '%' }"></div>
                  </div>
                  <span class="badge-progress-text">{{ badge.progress }}%</span>
                </div>
              </div>
            </div>

            <!-- Details -->
            <div class="card-footer">
              <div class="detail">
                <span>Matches:</span>
                <strong>{{ champion.matches }}</strong>
              </div>
              <div class="detail">
                <span>Winrate:</span>
                <strong :class="{ high: champion.winrate >= 50 }">{{ champion.winrate }}%</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mastery Details Table -->
    <div class="mastery-table-container">
      <h2>Detailed Mastery Stats</h2>
      <div class="table-scroll">
        <table class="mastery-table">
          <thead>
            <tr>
              <th>Champion</th>
              <th>Level</th>
              <th>Points</th>
              <th>Matches</th>
              <th>Winrate</th>
              <th>Progress</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="champion in sortedChampions" :key="champion.name">
              <td class="champ-name">{{ champion.emoji }} {{ champion.name }}</td>
              <td class="level">
                <span class="level-badge" :class="`level-${champion.level}`">{{ champion.level }}</span>
              </td>
              <td class="points">{{ champion.points }}</td>
              <td class="matches">{{ champion.matches }}</td>
              <td class="winrate" :class="{ high: champion.winrate >= 50 }">{{ champion.winrate }}%</td>
              <td class="progress">
                <div class="small-progress-bar">
                  <div class="progress-fill" :style="{ width: champion.progressPercent + '%' }"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Chart from 'chart.js/auto'

const router = useRouter()
const route = useRoute()

const riotId = computed(() => route.params.riotId || '')
const region = computed(() => route.params.region || '')

const goBack = () => {
  router.push({
    name: 'rewind',
    params: {
      riotId: riotId.value,
      region: region.value,
    },
  })
}

const selectedMasteryLevel = ref('All')
const selectedChampions = ref([])

// Sample mastery data with kill/assist tracking
const masteryData = ref([
  { name: 'Ahri', level: 7, points: 385000, matches: 120, winrate: 58, emoji: '🦊', totalKills: 1425, totalAssists: 892, progression: [0, 45000, 120000, 200000, 290000, 340000, 385000] },
  { name: 'Lux', level: 6, points: 280000, matches: 95, winrate: 62, emoji: '✨', totalKills: 645, totalAssists: 1240, progression: [0, 38000, 95000, 155000, 220000, 280000] },
  { name: 'Zed', level: 5, points: 185000, matches: 87, winrate: 55, emoji: '🥷', totalKills: 1687, totalAssists: 523, progression: [0, 42000, 98000, 150000, 185000] },
  { name: 'Yasuo', level: 6, points: 292000, matches: 110, winrate: 52, emoji: '⚔️', totalKills: 1532, totalAssists: 645, progression: [0, 35000, 88000, 145000, 215000, 292000] },
  { name: 'Evelynn', level: 5, points: 172000, matches: 78, winrate: 61, emoji: '👑', totalKills: 1123, totalAssists: 834, progression: [0, 40000, 92000, 135000, 172000] },
  { name: 'Akali', level: 4, points: 125000, matches: 65, winrate: 59, emoji: '🌸', totalKills: 987, totalAssists: 512, progression: [0, 38000, 82000, 125000] },
  { name: 'Sylas', level: 4, points: 112000, matches: 58, winrate: 54, emoji: '⛓️', totalKills: 845, totalAssists: 678, progression: [0, 35000, 75000, 112000] },
  { name: 'Qiyana', level: 3, points: 78000, matches: 42, winrate: 60, emoji: '💎', totalKills: 654, totalAssists: 423, progression: [0, 32000, 78000] },
])

// Get unique mastery levels
const masteryLevels = computed(() => {
  const levels = new Set(masteryData.value.map(c => c.level))
  return Array.from(levels).sort((a, b) => b - a)
})

// Determine rarity tier based on mastery level
const getRarityTier = (level) => {
  if (level === 7) return { rarity: 'diamond', name: 'Diamond' }
  if (level === 6) return { rarity: 'gold', name: 'Gold' }
  if (level === 5) return { rarity: 'silver', name: 'Silver' }
  if (level === 4) return { rarity: 'bronze', name: 'Bronze' }
  return { rarity: 'common', name: 'Common' }
}

// Generate badges with progression system (like 2K)
const generateBadges = (champion) => {
  const badges = []
  const avgKA = Math.round((champion.totalKills + champion.totalAssists) / champion.matches)

  // Kill Master Badge - Bronze to Diamond
  const killProgress = Math.min(100, Math.round((champion.totalKills / 1500) * 100))
  const killTier = champion.totalKills >= 1500 ? 'diamond' :
                   champion.totalKills >= 1200 ? 'gold' :
                   champion.totalKills >= 900 ? 'silver' : 'bronze'
  badges.push({
    name: 'Kill Master',
    tier: killTier,
    icon: '⚡',
    description: 'High kill count',
    progress: killProgress,
    requirement: `${champion.totalKills}/1500 kills`
  })

  // Team Player Badge - Bronze to Diamond
  const assistProgress = Math.min(100, Math.round((champion.totalAssists / 1000) * 100))
  const assistTier = champion.totalAssists >= 1000 ? 'diamond' :
                     champion.totalAssists >= 800 ? 'gold' :
                     champion.totalAssists >= 500 ? 'silver' : 'bronze'
  badges.push({
    name: 'Team Player',
    tier: assistTier,
    icon: '🤝',
    description: 'High assist count',
    progress: assistProgress,
    requirement: `${champion.totalAssists}/1000 assists`
  })

  // Dominant Badge - Win Rate progression
  const winRateProgress = Math.min(100, champion.winrate)
  const winTier = champion.winrate >= 60 ? 'diamond' :
                  champion.winrate >= 55 ? 'gold' :
                  champion.winrate >= 50 ? 'silver' : 'bronze'
  badges.push({
    name: 'Dominant',
    tier: winTier,
    icon: '👑',
    description: 'Win rate progression',
    progress: winRateProgress,
    requirement: `${champion.winrate}% win rate`
  })

  // Veteran Badge - Match progression
  const matchProgress = Math.min(100, Math.round((champion.matches / 150) * 100))
  const matchTier = champion.matches >= 150 ? 'diamond' :
                    champion.matches >= 120 ? 'gold' :
                    champion.matches >= 60 ? 'silver' : 'bronze'
  badges.push({
    name: 'Veteran',
    tier: matchTier,
    icon: '🎖️',
    description: 'Match experience',
    progress: matchProgress,
    requirement: `${champion.matches}/150 matches`
  })

  // Decisive Badge - K/A Ratio progression
  const ratioProgress = Math.min(100, Math.round((avgKA / 20) * 100))
  const ratiTier = avgKA >= 20 ? 'diamond' :
                   avgKA >= 18 ? 'gold' :
                   avgKA >= 15 ? 'silver' : 'bronze'
  badges.push({
    name: 'Decisive',
    tier: ratiTier,
    icon: '🎯',
    description: 'High K/A ratio',
    progress: ratioProgress,
    requirement: `${avgKA}/20 K/A ratio`
  })

  return badges
}

// Selection functions
const selectAllChampions = () => {
  selectedChampions.value = masteryData.value.map(c => c.name)
}

const clearSelection = () => {
  selectedChampions.value = []
}

// Get selected champions data for display
const selectedChampionsData = computed(() => {
  if (selectedChampions.value.length === 0) return []
  return masteryData.value.filter(c => selectedChampions.value.includes(c.name))
})

// Top champions cards (only show when exactly one is selected)
const topChampionsCards = computed(() => {
  // If exactly one champion is selected, show their details
  if (selectedChampions.value.length === 1) {
    const selectedChamp = masteryData.value.find(c => c.name === selectedChampions.value[0])
    if (!selectedChamp) return []

    const rarity = getRarityTier(selectedChamp.level)
    const kaRatio = (selectedChamp.totalKills + selectedChamp.totalAssists) / selectedChamp.matches
    return [{
      ...selectedChamp,
      ...rarity,
      rarityName: rarity.name,
      kaRatio: kaRatio.toFixed(1),
      badges: generateBadges(selectedChamp),
    }]
  }

  // Default: show top 5 (won't be displayed due to v-if)
  return masteryData.value
    .sort((a, b) => b.points - a.points)
    .slice(0, 5)
    .map(champion => {
      const rarity = getRarityTier(champion.level)
      const kaRatio = (champion.totalKills + champion.totalAssists) / champion.matches
      return {
        ...champion,
        ...rarity,
        rarityName: rarity.name,
        kaRatio: kaRatio.toFixed(1),
        badges: generateBadges(champion),
      }
    })
})

// Sorted champions by points (descending)
const sortedChampions = computed(() => {
  return [...masteryData.value].sort((a, b) => b.points - a.points)
})

// Calculate stats
const masteredChampions = computed(() => {
  return masteryData.value.filter(c => c.level >= 5)
})

const totalMasteryPoints = computed(() => {
  return masteryData.value.reduce((sum, c) => sum + c.points, 0)
})

const avgMasteryLevel = computed(() => {
  if (masteryData.value.length === 0) return 0
  const avg = masteryData.value.reduce((sum, c) => sum + c.level, 0) / masteryData.value.length
  return avg.toFixed(1)
})

const topChampion = computed(() => {
  if (masteryData.value.length === 0) return 'N/A'
  return masteryData.value.reduce((top, c) => c.points > top.points ? c : top).name
})


const progressionChart = ref(null)

// Initialize progression chart
onMounted(() => {
  initProgressionChart()
})

// Watch for changes in selected champions and reinitialize chart
watch(selectedChampions, () => {
  initProgressionChart()
})

const initProgressionChart = () => {
  if (!progressionChart.value) return

  if (progressionChart.value.chart) {
    progressionChart.value.chart.destroy()
  }

  const ctx = progressionChart.value.getContext('2d')

  const championsToDisplay = selectedChampionsData.value.length > 0 ? selectedChampionsData.value : []
  const displayChampions = championsToDisplay.slice(0, 8) // Limit to 8 champions for readability

  if (displayChampions.length === 0) {
    return
  }

  // Find the maximum progression array length to determine labels
  const maxLength = Math.max(...displayChampions.map(c => c.progression.length))
  const weeks = Array.from({ length: maxLength }, (_, i) => `Week ${i + 1}`)

  const colors = ['#a855f7', '#06b6d4', '#86efac', '#fca5a5', '#fbbf24', '#ec4899', '#f59e0b', '#8b5cf6']

  const datasets = displayChampions.map((champion, idx) => {
    const color = colors[idx % colors.length]
    return {
      label: champion.name,
      data: champion.progression,
      borderColor: color,
      backgroundColor: color + '22',
      borderWidth: 2.5,
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: color,
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6,
    }
  })

  const chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: weeks,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            color: '#cbd5e1',
            font: { size: 12, weight: 'bold' },
            padding: 15,
            usePointStyle: true,
            pointStyle: 'circle',
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: '#94a3b8',
            font: { size: 11 },
            callback: function(value) {
              return (value / 1000) + 'K'
            },
          },
          grid: {
            color: 'rgba(99, 102, 241, 0.1)',
            drawBorder: false,
          },
        },
        x: {
          ticks: {
            color: '#94a3b8',
            font: { size: 11 },
          },
          grid: {
            color: 'transparent',
            drawBorder: false,
          },
        },
      },
    },
  })

  progressionChart.value.chart = chartInstance
}
</script>

<style scoped>
.mastery-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27, #1a1f3a, #0f1628);
  padding: 40px 20px;
}

.mastery-header {
  margin-bottom: 40px;
  animation: slideDown 0.6s ease-out;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.back-btn {
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #e2e8f0;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(99, 102, 241, 0.4);
  border-color: rgba(99, 102, 241, 0.6);
  transform: translateX(-4px);
}

.spacer {
  width: 60px;
}

.mastery-header h1 {
  font-size: 2.5rem;
  color: #e2e8f0;
  margin: 0;
  font-weight: 700;
  text-align: center;
}

.subtitle {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0;
  text-align: center;
}

/* Mastery Stats */
.mastery-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}

.stat-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.stat-card:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(168, 85, 247, 0.4);
  transform: translateY(-4px);
}

.stat-label {
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  font-weight: 600;
}

.stat-value {
  color: #a78bfa;
  font-size: 2rem;
  font-weight: 700;
}

/* Champion Selection */
.champion-selection {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 40px;
  backdrop-filter: blur(10px);
}

.champion-selection h2 {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.selection-subtitle {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0 0 20px 0;
}

.champion-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.champion-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.champion-checkbox:hover {
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.4);
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #6366f1;
}

.checkbox-label {
  color: #cbd5e1;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
}

.level-info {
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: auto;
  background: rgba(99, 102, 241, 0.2);
  padding: 2px 8px;
  border-radius: 4px;
}

.selection-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.action-btn:hover {
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.action-btn.secondary {
  background: rgba(99, 102, 241, 0.2);
  color: #cbd5e1;
}

.action-btn.secondary:hover {
  background: rgba(99, 102, 241, 0.3);
  border-color: rgba(99, 102, 241, 0.5);
}

/* No Selection Message */
.no-selection {
  background: rgba(30, 41, 59, 0.6);
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  margin-bottom: 40px;
}

.no-selection p {
  color: #94a3b8;
  font-size: 1.1rem;
  margin: 0;
}

.chart-subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0 0 20px 0;
}

/* Progression Chart */
.progression-container {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 40px;
  backdrop-filter: blur(10px);
}

.progression-container h2 {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.chart-holder {
  position: relative;
  height: 400px;
  width: 100%;
}

.chart-holder canvas {
  max-width: 100%;
}

/* Champions Section (2K Style) */
.champions-section {
  margin-bottom: 40px;
}

.champions-section h2 {
  color: #e2e8f0;
  font-size: 1.8rem;
  margin: 0 0 30px 0;
  font-weight: 700;
}

.champions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

/* 2K Style Player Card */
.player-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border: 2px solid rgba(99, 102, 241, 0.2);
}

.player-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);
}

/* Rarity Colors */
.player-card.rarity-diamond {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 193, 7, 0.1));
  border-color: rgba(255, 215, 0, 0.4);
}

.player-card.rarity-gold {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(217, 70, 239, 0.1));
  border-color: rgba(168, 85, 247, 0.4);
}

.player-card.rarity-silver {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.1));
  border-color: rgba(59, 130, 246, 0.4);
}

.player-card.rarity-bronze {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.1));
  border-color: rgba(34, 197, 94, 0.4);
}

.card-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: radial-gradient(circle at top right, rgba(168, 85, 247, 0.2), transparent);
  pointer-events: none;
}

.card-content {
  position: relative;
  z-index: 1;
  padding: 20px;
}

.card-header {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  align-items: flex-start;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  font-size: 3.5rem;
  display: block;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 2px solid rgba(168, 85, 247, 0.3);
}

.level-indicator {
  position: absolute;
  bottom: -5px;
  right: -5px;
  background: linear-gradient(135deg, #ffd700, #ffb700);
  color: #1a1a1a;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1rem;
  border: 2px solid rgba(255, 215, 0, 0.6);
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
}

.name-section {
  flex: 1;
}

.champion-name {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.rarity-name {
  color: #94a3b8;
  font-size: 0.85rem;
  margin: 4px 0 0 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(99, 102, 241, 0.1);
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-label {
  color: #94a3b8;
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-bottom: 6px;
}

.stat-value {
  color: #a78bfa;
  font-size: 1.3rem;
  font-weight: 700;
}

/* Badges Container with Progression */
.badges-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 20px;
  margin-bottom: 16px;
  padding: 16px 0;
}

.achievement-badge-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.achievement-badge-wrapper.achieved {
  opacity: 1;
}

.achievement-badge {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
  font-size: 0.7rem;
}

.achievement-badge:hover {
  transform: scale(1.1);
}

.badge-icon {
  font-size: 1.4rem;
  line-height: 1;
}

.badge-tier {
  font-weight: 800;
  font-size: 0.65rem;
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.5);
  padding: 1px 3px;
  border-radius: 3px;
}

.badge-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
  width: 100%;
}

.badge-progress-bar {
  width: 80px;
  height: 4px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 2px;
  overflow: hidden;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.badge-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #a855f7, #d946ef);
  transition: width 0.3s ease;
  box-shadow: 0 0 4px rgba(168, 85, 247, 0.6);
}

.badge-progress-text {
  color: #94a3b8;
  font-size: 0.7rem;
  font-weight: 600;
}

.badge-gold {
  background: rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.6);
  color: #ffd700;
  box-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
}

.badge-silver {
  background: rgba(192, 192, 192, 0.2);
  border-color: rgba(192, 192, 192, 0.6);
  color: #c0c0c0;
  box-shadow: 0 0 8px rgba(192, 192, 192, 0.3);
}

.badge-diamond {
  background: rgba(100, 200, 255, 0.2);
  border-color: rgba(100, 200, 255, 0.6);
  color: #64c8ff;
  box-shadow: 0 0 8px rgba(100, 200, 255, 0.3);
}

.badge-bronze {
  background: rgba(205, 127, 50, 0.2);
  border-color: rgba(205, 127, 50, 0.6);
  color: #cd7f32;
  box-shadow: 0 0 8px rgba(205, 127, 50, 0.3);
}

/* Card Footer */
.card-footer {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  font-size: 0.9rem;
}

.detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.detail span {
  color: #94a3b8;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: 600;
  margin-bottom: 4px;
}

.detail strong {
  color: #a78bfa;
  font-size: 1.1rem;
  font-weight: 700;
}

.detail strong.high {
  color: #86efac;
}

/* Mastery Table */
.mastery-table-container {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  backdrop-filter: blur(10px);
}

.mastery-table-container h2 {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.table-scroll {
  overflow-x: auto;
}

.mastery-table {
  width: 100%;
  border-collapse: collapse;
}

.mastery-table thead {
  background: rgba(99, 102, 241, 0.1);
}

.mastery-table th {
  color: #a78bfa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.mastery-table td {
  color: #cbd5e1;
  padding: 12px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  font-size: 0.9rem;
}

.mastery-table tbody tr:hover {
  background: rgba(99, 102, 241, 0.1);
}

.champ-name {
  color: #e2e8f0;
  font-weight: 600;
}

.level {
  text-align: center;
}

.level-badge {
  background: linear-gradient(135deg, #a855f7, #d946ef);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
}

.level-badge.level-7 {
  background: linear-gradient(135deg, #ffd700, #ffb700);
}

.level-badge.level-6 {
  background: linear-gradient(135deg, #a855f7, #d946ef);
}

.level-badge.level-5 {
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
}

.level-badge.level-4 {
  background: linear-gradient(135deg, #22c55e, #84cc16);
}

.level-badge.level-3 {
  background: linear-gradient(135deg, #a8a2a2, #d4d4d4);
}

.points,
.matches {
  text-align: center;
  color: #a78bfa;
  font-weight: 600;
}

.winrate {
  text-align: center;
  color: #fca5a5;
  font-weight: 600;
}

.winrate.high {
  color: #86efac;
}

.progress {
  text-align: center;
}

.small-progress-bar {
  background: rgba(0, 0, 0, 0.3);
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  display: inline-block;
  width: 120px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.small-progress-bar .progress-fill {
  height: 100%;
  border-radius: 3px;
}

/* Animations */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .mastery-container {
    padding: 20px 10px;
  }

  .mastery-header h1 {
    font-size: 2rem;
  }

  .champions-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .name-section {
    width: 100%;
  }

  .champion-name {
    font-size: 1.3rem;
  }

  .avatar {
    width: 70px;
    height: 70px;
    font-size: 3rem;
  }

  .stats-row {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .mastery-table th,
  .mastery-table td {
    padding: 8px;
    font-size: 0.8rem;
  }

  .chart-holder {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .mastery-container {
    padding: 15px 5px;
  }

  .mastery-header h1 {
    font-size: 1.5rem;
  }

  .champions-grid {
    grid-template-columns: 1fr;
  }

  .card-content {
    padding: 16px;
  }

  .avatar {
    width: 60px;
    height: 60px;
    font-size: 2.5rem;
  }

  .champion-name {
    font-size: 1.1rem;
  }

  .stats-row {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    padding: 12px;
  }

  .stat-label {
    font-size: 0.65rem;
  }

  .stat-value {
    font-size: 1.1rem;
  }

  .badges-container {
    gap: 6px;
  }

  .achievement-badge {
    width: 36px;
    height: 36px;
  }

  .badge-icon {
    font-size: 1rem;
  }

  .mastery-stats {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .chart-holder {
    height: 250px;
  }
}
</style>
