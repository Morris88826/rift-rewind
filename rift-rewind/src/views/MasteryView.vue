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

    <!-- Mastery Progression Chart -->
    <div class="progression-container" v-if="selectedChampions.length > 0">
      <div class="progression-header">
        <div>
          <h2>Mastery Progression Over Time</h2>
          <p class="chart-subtitle">{{ selectedChampions[0] }}'s progression</p>
        </div>
        <div class="chart-controls">
          <button
            @click="chartTimeframe = 'month'"
            :class="{ active: chartTimeframe === 'month' }"
            class="timeframe-btn"
          >
            📅 Month
          </button>
          <button
            @click="chartTimeframe = 'week'"
            :class="{ active: chartTimeframe === 'week' }"
            class="timeframe-btn"
          >
            📊 Week
          </button>
        </div>
      </div>
      <div class="chart-holder">
        <canvas ref="progressionChart"></canvas>
      </div>
    </div>

    <div v-else class="no-selection">
      <p>👆 Click a champion card above to view their progression</p>
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
              <div v-for="badge in champion.badges" :key="badge.name" class="achievement-badge-wrapper" :class="{ achieved: badge.progress > 0 || badge.alwaysActive }">
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

    <!-- Mastery Details Grid -->
    <div class="mastery-stats-section">
      <h2>Champion Mastery Stats</h2>
      <div class="stats-grid">
        <div v-for="champion in sortedChampions" :key="champion.name" class="stat-card" :class="{ selected: selectedChampions[0] === champion.name }" @click="selectChampion(champion.name)">
          <div class="card-header">
            <div class="champion-info">
              <span class="champion-emoji">{{ champion.emoji }}</span>
              <span class="champion-name">{{ champion.name }}</span>
            </div>
            <span class="level-badge" :class="`level-${champion.level}`">Lv {{ champion.level }}</span>
          </div>

          <div class="card-body">
            <div class="stat-row">
              <div class="stat-item">
                <span class="stat-label">Points</span>
                <span class="stat-value points">{{ champion.points.toLocaleString() }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Matches</span>
                <span class="stat-value matches">{{ champion.matches }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Winrate</span>
                <span class="stat-value winrate" :class="{ high: champion.winrate >= 50 }">{{ champion.winrate }}%</span>
              </div>
            </div>

            <div class="progress-section">
              <span class="progress-label">Mastery Progress</span>
              <div class="progress-bar-container">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: champion.progressPercent + '%' }"></div>
                </div>
                <span class="progress-percent">{{ champion.progressPercent }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
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

// Default to first champion from masteryData
const selectedChampions = ref([masteryData.value[0].name])

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

  // Reliable Badge - Always Active (participation)
  const reliabilityScore = Math.min(100, Math.round((champion.matches / 50) * 100))
  const reliabilityTier = champion.matches >= 150 ? 'diamond' :
                          champion.matches >= 100 ? 'gold' :
                          champion.matches >= 50 ? 'silver' : 'bronze'
  badges.push({
    name: 'Reliable',
    tier: reliabilityTier,
    icon: '📍',
    description: 'Consistent performer',
    progress: reliabilityScore,
    requirement: `${champion.matches}/150 participations`,
    alwaysActive: true
  })

  // Momentum Badge - Points progression
  const pointsPerMatch = Math.round(champion.points / champion.matches)
  const momentumProgress = Math.min(100, Math.round((pointsPerMatch / 3000) * 100))
  const momentumTier = pointsPerMatch >= 3000 ? 'diamond' :
                       pointsPerMatch >= 2500 ? 'gold' :
                       pointsPerMatch >= 2000 ? 'silver' : 'bronze'
  badges.push({
    name: 'Momentum',
    tier: momentumTier,
    icon: '📈',
    description: 'Points per match',
    progress: momentumProgress,
    requirement: `${pointsPerMatch} points/match`
  })

  // Clutch Badge - Based on win rate (close wins)
  const clutchProgress = Math.min(100, champion.winrate)
  const clutchTier = champion.winrate >= 60 ? 'diamond' :
                     champion.winrate >= 55 ? 'gold' :
                     champion.winrate >= 50 ? 'silver' : 'bronze'
  badges.push({
    name: 'Clutch',
    tier: clutchTier,
    icon: '🔥',
    description: 'Clutch performance',
    progress: clutchProgress,
    requirement: `${champion.winrate}% clutch wins`,
    alwaysActive: true
  })

  // Elite Badge - Overall mastery level (always active if level > 0)
  const eliteProgress = Math.min(100, champion.level * 14.28)
  const eliteTier = champion.level === 7 ? 'diamond' :
                    champion.level === 6 ? 'gold' :
                    champion.level === 5 ? 'silver' : 'bronze'
  badges.push({
    name: 'Elite',
    tier: eliteTier,
    icon: '💎',
    description: 'Mastery level',
    progress: eliteProgress,
    requirement: `Level ${champion.level}/7`,
    alwaysActive: true
  })

  // Engagement Badge - Kills + Assists combined
  const engagementScore = Math.round((champion.totalKills + champion.totalAssists) / 2)
  const engagementProgress = Math.min(100, Math.round((engagementScore / 2000) * 100))
  const engagementTier = engagementScore >= 2000 ? 'diamond' :
                         engagementScore >= 1500 ? 'gold' :
                         engagementScore >= 1000 ? 'silver' : 'bronze'
  badges.push({
    name: 'Engagement',
    tier: engagementTier,
    icon: '⚔️',
    description: 'Combat engagement',
    progress: engagementProgress,
    requirement: `${engagementScore} total impact`
  })

  return badges
}

// Selection function
const selectChampion = (championName) => {
  selectedChampions.value = [championName]
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
  return [...masteryData.value].sort((a, b) => b.points - a.points).map(c => ({
    ...c,
    progressPercent: Math.min(100, Math.round((c.level / 7) * 100))
  }))
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
const chartTimeframe = ref('month')

// Initialize progression chart
onMounted(() => {
  initProgressionChart()
})

// Watch for changes in selected champions and reinitialize chart
watch(selectedChampions, async () => {
  await nextTick()
  initProgressionChart()
})

// Watch for timeframe changes and redraw chart
watch(chartTimeframe, async () => {
  await nextTick()
  initProgressionChart()
})

const initProgressionChart = () => {
  // Wait for canvas to be available
  if (!progressionChart.value) {
    return
  }

  // Get the canvas element itself
  const canvasElement = progressionChart.value
  if (!canvasElement) return

  // Destroy existing chart
  if (canvasElement.chart) {
    canvasElement.chart.destroy()
    canvasElement.chart = null
  }

  const ctx = canvasElement.getContext('2d')
  if (!ctx) return

  const championsToDisplay = selectedChampionsData.value && selectedChampionsData.value.length > 0 ? selectedChampionsData.value : []

  if (championsToDisplay.length === 0) {
    return
  }

  const displayChampions = championsToDisplay.slice(0, 8) // Limit to 8 champions for readability

  // Find the maximum progression array length to determine labels
  const maxLength = Math.max(...displayChampions.map(c => c.progression.length))

  // Prepare labels and data based on timeframe
  let labels = []
  const weeksPerMonth = 4
  const samplingInterval = chartTimeframe.value === 'month' ? weeksPerMonth : 1

  if (chartTimeframe.value === 'month') {
    // Create month labels
    for (let i = 0; i < maxLength; i += weeksPerMonth) {
      const monthIndex = Math.floor(i / weeksPerMonth) + 1
      labels.push(`Month ${monthIndex}`)
    }
  } else {
    // Create week labels
    labels = Array.from({ length: maxLength }, (_, i) => `Week ${i + 1}`)
  }

  const colors = ['#a855f7', '#06b6d4', '#86efac', '#fca5a5', '#fbbf24', '#ec4899', '#f59e0b', '#8b5cf6']

  const datasets = displayChampions.map((champion, idx) => {
    const color = colors[idx % colors.length]
    let progressionData = []

    if (chartTimeframe.value === 'month') {
      // Sample data at monthly intervals (every 4 weeks)
      for (let i = 0; i < champion.progression.length; i += weeksPerMonth) {
        progressionData.push(champion.progression[i])
      }
      // Ensure we have the final value
      if (progressionData[progressionData.length - 1] !== champion.progression[champion.progression.length - 1]) {
        progressionData.push(champion.progression[champion.progression.length - 1])
      }
    } else {
      // Show all weekly data
      progressionData = champion.progression
    }

    return {
      label: champion.name,
      data: progressionData,
      borderColor: color,
      backgroundColor: color + '22',
      borderWidth: 2.5,
      fill: true,
      tension: 0.4,
      pointRadius: chartTimeframe.value === 'month' ? 5 : 3,
      pointBackgroundColor: color,
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6,
    }
  })

  const chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
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

.progression-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.progression-header > div:first-child h2 {
  margin: 0 0 8px 0;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.timeframe-btn {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: #cbd5e1;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
}

.timeframe-btn:hover {
  border-color: rgba(99, 102, 241, 0.6);
  background: rgba(99, 102, 241, 0.2);
  color: #f1f5f9;
}

.timeframe-btn.active {
  background: linear-gradient(135deg, #a855f7, #d946ef);
  border-color: rgba(168, 85, 247, 0.8);
  color: white;
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
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

/* Mastery Stats Section */
.mastery-stats-section {
  margin-bottom: 40px;
}

.mastery-stats-section h2 {
  color: #f1f5f9;
  font-size: 1.8rem;
  margin: 0 0 32px 0;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.stat-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(20, 25, 50, 0.9));
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  border-color: rgba(99, 102, 241, 0.6);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.2);
  transform: translateY(-4px);
  cursor: pointer;
}

.stat-card.selected {
  border-color: rgba(99, 102, 241, 0.8);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.1));
  box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3), inset 0 0 20px rgba(99, 102, 241, 0.1);
}

.stat-card.selected:hover {
  border-color: rgba(99, 102, 241, 0.9);
  box-shadow: 0 14px 48px rgba(99, 102, 241, 0.4), inset 0 0 20px rgba(99, 102, 241, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.champion-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.champion-emoji {
  font-size: 2rem;
  line-height: 1;
}

.champion-name {
  color: #f1f5f9;
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: 0.3px;
}

.level-badge {
  background: linear-gradient(135deg, #a855f7, #d946ef);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 800;
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
  letter-spacing: 0.5px;
}

.level-badge.level-7 {
  background: linear-gradient(135deg, #ffd700, #ffb700);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.level-badge.level-6 {
  background: linear-gradient(135deg, #a855f7, #d946ef);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
}

.level-badge.level-5 {
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.level-badge.level-4 {
  background: linear-gradient(135deg, #22c55e, #84cc16);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.level-badge.level-3 {
  background: linear-gradient(135deg, #94a3b8, #cbd5e1);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.3);
}

.card-body {
  padding: 20px;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stat-label {
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.stat-value {
  color: #f1f5f9;
  font-size: 1.3rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.stat-value.points {
  color: #fbbf24;
}

.stat-value.matches {
  color: #a78bfa;
}

.stat-value.winrate {
  color: #f87171;
}

.stat-value.winrate.high {
  color: #86efac;
}

.progress-section {
  border-top: 1px solid rgba(99, 102, 241, 0.2);
  padding-top: 16px;
}

.progress-label {
  display: block;
  color: #cbd5e1;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.progress-bar-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  background: rgba(15, 23, 42, 0.8);
  height: 8px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(99, 102, 241, 0.3);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #a855f7, #d946ef);
  border-radius: 6px;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.6);
  transition: width 0.4s ease;
}

.progress-percent {
  color: #a78bfa;
  font-size: 0.9rem;
  font-weight: 700;
  min-width: 35px;
  text-align: right;
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
