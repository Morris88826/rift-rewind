<template>
  <div class="infographic-container">
    <div class="infographic-header">
      <div class="header-top">
        <button @click="goBack" class="back-btn">← Back</button>
        <h1>Performance Infographic</h1>
        <div class="spacer"></div>
      </div>
      <p class="subtitle">Analyze your gameplay with interactive radar charts</p>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="filter-header">
        <h3>Filters</h3>
        <button
          @click="filterExpanded = !filterExpanded"
          class="filter-toggle"
          :class="{ collapsed: !filterExpanded }"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
      </div>

      <div v-show="filterExpanded" class="filter-content">
        <div class="filter-group">
          <label class="filter-label">Lane</label>
          <div class="filter-buttons">
            <button
              v-for="lane in lanes"
              :key="lane"
              @click="selectedLane = lane"
              class="filter-btn"
              :class="{ active: selectedLane === lane }"
            >
              {{ lane }}
            </button>
            <button
              @click="selectedLane = 'All'"
              class="filter-btn"
              :class="{ active: selectedLane === 'All' }"
            >
              All
            </button>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Champion</label>
          <div class="filter-buttons">
            <button
              v-for="champion in availableChampions"
              :key="champion"
              @click="selectedChampion = champion"
              class="filter-btn champion-btn"
              :class="{ active: selectedChampion === champion }"
            >
              {{ champion }}
            </button>
            <button
              @click="selectedChampion = 'All'"
              class="filter-btn"
              :class="{ active: selectedChampion === 'All' }"
            >
              All
            </button>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Game Mode</label>
          <div class="filter-buttons">
            <button
              v-for="mode in gameModes"
              :key="mode"
              @click="selectedMode = mode"
              class="filter-btn"
              :class="{ active: selectedMode === mode }"
            >
              {{ mode }}
            </button>
            <button
              @click="selectedMode = 'All'"
              class="filter-btn"
              :class="{ active: selectedMode === 'All' }"
            >
              All
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div class="stat-card">
        <div class="stat-label">Matches Analyzed</div>
        <div class="stat-value">{{ filteredMatches.length }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Win Rate</div>
        <div class="stat-value">{{ winRate }}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Avg K/D/A</div>
        <div class="stat-value">{{ avgKDA }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Avg CS</div>
        <div class="stat-value">{{ avgCS }}</div>
      </div>
    </div>

    <!-- Champion Card + Radar Layout -->
    <div class="champion-radar-wrapper">
      <!-- Left: Champion Card (only when champion selected) -->
      <div v-if="selectedChampion !== 'All'" class="champion-card-left">
        <div class="champion-card">
          <div class="champion-icon">👤</div>
          <h2 class="champion-name">{{ selectedChampion }}</h2>
          <div class="champion-matches">{{ championMatches.length }} Matches</div>

          <div class="quick-stats">
            <div class="quick-stat">
              <span class="qs-label">Win Rate</span>
              <span class="qs-value" :class="{ high: championWinRate >= 50 }">{{ championWinRate }}%</span>
            </div>
            <div class="quick-stat">
              <span class="qs-label">K/D/A</span>
              <span class="qs-value">{{ championAvgKDA }}</span>
            </div>
            <div class="quick-stat">
              <span class="qs-label">Avg CS</span>
              <span class="qs-value">{{ championAvgCS }}</span>
            </div>
            <div class="quick-stat">
              <span class="qs-label">Avg Gold</span>
              <span class="qs-value">{{ championAvgGold }}</span>
            </div>
            <div class="quick-stat">
              <span class="qs-label">Avg DMG</span>
              <span class="qs-value">{{ championAvgDamage }}</span>
            </div>
            <div class="quick-stat">
              <span class="qs-label">Participation</span>
              <span class="qs-value">{{ championAvgParticipation }}%</span>
            </div>
          </div>

          <div class="lanes-played">
            <span class="breakdown-label">Lanes:</span>
            <div class="lane-badges">
              <span v-for="lane in championLanes" :key="lane" class="lane-badge">{{ lane }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Radar Chart (always visible) -->
      <div class="chart-container" :class="{ 'full-width': selectedChampion === 'All' }">
        <div class="chart-wrapper">
          <h2>Performance Radar</h2>
          <div class="legend-info">
            <span class="legend-item your"><span class="legend-dot"></span>Your Performance</span>
            <span class="legend-item average"><span class="legend-dot"></span>Average Performance</span>
          </div>
          <div class="canvas-container">
            <canvas ref="radarChart"></canvas>
          </div>
        </div>

        <!-- Performance Comparison -->
        <div class="performance-comparison">
          <h3>Comparison vs Average</h3>
          <div class="comparison-grid">
            <div v-for="(label, idx) in comparisonMetrics" :key="idx" class="comparison-item">
              <div class="metric-name">{{ label }}</div>
              <div class="metric-bars">
                <div class="bar-container">
                  <div class="bar your" :style="{ width: yourPerformancePercent[idx] + '%' }"></div>
                </div>
                <div class="bar-container">
                  <div class="bar average" :style="{ width: averagePerformancePercent[idx] + '%' }"></div>
                </div>
              </div>
              <div class="metric-diff" :class="{ positive: performanceDiff[idx] >= 0 }">
                {{ performanceDiff[idx] >= 0 ? '+' : '' }}{{ performanceDiff[idx] }}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Stats Table -->
    <div class="stats-table-container">
      <h2>Detailed Statistics</h2>
      <div class="table-scroll">
        <table class="stats-table">
          <thead>
            <tr>
              <th>Champion</th>
              <th>Lane</th>
              <th>Mode</th>
              <th>K/D/A</th>
              <th>CS</th>
              <th>Win Rate</th>
              <th>Games</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stat in detailedStats" :key="`${stat.champion}-${stat.lane}-${stat.mode}`">
              <td>{{ stat.champion }}</td>
              <td>{{ stat.lane }}</td>
              <td>{{ stat.mode }}</td>
              <td class="kda">{{ stat.avgKDA }}</td>
              <td class="cs">{{ stat.avgCS }}</td>
              <td class="winrate" :class="{ high: stat.winRate >= 50 }">{{ stat.winRate }}%</td>
              <td class="games">{{ stat.games }}</td>
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

// Filter state
const selectedLane = ref('All')
const selectedChampion = ref('All')
const selectedMode = ref('All')
const filterExpanded = ref(false)

// Available options
const lanes = ['Mid', 'Support', 'ADC', 'Top', 'Jungle']
const gameModes = ['Ranked', 'Unranked', 'ARAM']

// Sample match data with more details
const matchData = ref([
  { champion: 'Ahri', lane: 'Mid', mode: 'Ranked', kills: 12, deaths: 2, assists: 8, cs: 287, gold: 14500, damage: 18000, participation: 85 },
  { champion: 'Ahri', lane: 'Mid', mode: 'Ranked', kills: 7, deaths: 5, assists: 14, cs: 256, gold: 12300, damage: 15000, participation: 92 },
  { champion: 'Lux', lane: 'Support', mode: 'Ranked', kills: 3, deaths: 1, assists: 21, cs: 45, gold: 8200, damage: 12000, participation: 95 },
  { champion: 'Ahri', lane: 'Mid', mode: 'Ranked', kills: 15, deaths: 3, assists: 12, cs: 312, gold: 15800, damage: 19000, participation: 88 },
  { champion: 'Lux', lane: 'Support', mode: 'Ranked', kills: 2, deaths: 2, assists: 18, cs: 52, gold: 8500, damage: 11000, participation: 90 },
  { champion: 'Ahri', lane: 'Mid', mode: 'Ranked', kills: 8, deaths: 6, assists: 10, cs: 278, gold: 13000, damage: 16000, participation: 80 },
  { champion: 'Zed', lane: 'Mid', mode: 'Ranked', kills: 18, deaths: 2, assists: 5, cs: 334, gold: 16500, damage: 21000, participation: 75 },
  { champion: 'Ahri', lane: 'Mid', mode: 'Unranked', kills: 10, deaths: 4, assists: 9, cs: 295, gold: 14200, damage: 17000, participation: 82 },
  { champion: 'Lux', lane: 'Support', mode: 'ARAM', kills: 4, deaths: 1, assists: 25, cs: 58, gold: 9000, damage: 13000, participation: 98 },
  { champion: 'Ahri', lane: 'Mid', mode: 'Ranked', kills: 11, deaths: 3, assists: 11, cs: 305, gold: 15100, damage: 18500, participation: 86 },
])

// Get unique champions from data
const availableChampions = computed(() => {
  const champs = new Set(matchData.value.map(m => m.champion))
  return Array.from(champs).sort()
})

// Filter matches based on selections
const filteredMatches = computed(() => {
  return matchData.value.filter(match => {
    const laneMatch = selectedLane.value === 'All' || match.lane === selectedLane.value
    const champMatch = selectedChampion.value === 'All' || match.champion === selectedChampion.value
    const modeMatch = selectedMode.value === 'All' || match.mode === selectedMode.value
    return laneMatch && champMatch && modeMatch
  })
})

// Calculate statistics
const winRate = computed(() => {
  if (filteredMatches.value.length === 0) return 0
  const wins = filteredMatches.value.filter(m => (m.kills + m.assists) > m.deaths * 2).length
  return Math.round((wins / filteredMatches.value.length) * 100)
})

const avgKDA = computed(() => {
  if (filteredMatches.value.length === 0) return '0.0'
  const total = filteredMatches.value.reduce((sum, m) => sum + (m.kills + m.assists) / Math.max(1, m.deaths), 0)
  return (total / filteredMatches.value.length).toFixed(1)
})

const avgCS = computed(() => {
  if (filteredMatches.value.length === 0) return '0'
  const total = filteredMatches.value.reduce((sum, m) => sum + m.cs, 0)
  return Math.round(total / filteredMatches.value.length)
})

// Champion-specific stats
const championMatches = computed(() => {
  if (selectedChampion.value === 'All') return []
  return filteredMatches.value.filter(m => m.champion === selectedChampion.value)
})

const championWinRate = computed(() => {
  if (championMatches.value.length === 0) return 0
  const wins = championMatches.value.filter(m => (m.kills + m.assists) > m.deaths * 2).length
  return Math.round((wins / championMatches.value.length) * 100)
})

const championAvgKDA = computed(() => {
  if (championMatches.value.length === 0) return '0.0'
  const total = championMatches.value.reduce((sum, m) => sum + (m.kills + m.assists) / Math.max(1, m.deaths), 0)
  return (total / championMatches.value.length).toFixed(1)
})

const championAvgCS = computed(() => {
  if (championMatches.value.length === 0) return '0'
  const total = championMatches.value.reduce((sum, m) => sum + m.cs, 0)
  return Math.round(total / championMatches.value.length)
})

const championAvgGold = computed(() => {
  if (championMatches.value.length === 0) return '0'
  const total = championMatches.value.reduce((sum, m) => sum + m.gold, 0)
  return Math.round(total / championMatches.value.length)
})

const championAvgDamage = computed(() => {
  if (championMatches.value.length === 0) return '0'
  const total = championMatches.value.reduce((sum, m) => sum + m.damage, 0)
  return Math.round(total / championMatches.value.length)
})

const championAvgParticipation = computed(() => {
  if (championMatches.value.length === 0) return 0
  const total = championMatches.value.reduce((sum, m) => sum + m.participation, 0)
  return Math.round(total / championMatches.value.length)
})

const championLanes = computed(() => {
  if (championMatches.value.length === 0) return []
  const lanes = new Set(championMatches.value.map(m => m.lane))
  return Array.from(lanes).sort()
})

// Normalize value to 0-100 scale
const normalizeValue = (value, max) => {
  return Math.min(100, (value / max) * 100)
}

// Calculate radar chart data
const radarData = computed(() => {
  if (filteredMatches.value.length === 0) {
    return {
      labels: [],
      yourData: [0, 0, 0, 0, 0],
      averageData: [0, 0, 0, 0, 0]
    }
  }

  // Calculate your performance (filtered)
  const yourKDAScore = filteredMatches.value.reduce((sum, m) => sum + (m.kills + m.assists) / Math.max(1, m.deaths), 0) / filteredMatches.value.length
  const yourCSScore = filteredMatches.value.reduce((sum, m) => sum + m.cs, 0) / filteredMatches.value.length
  const yourGold = filteredMatches.value.reduce((sum, m) => sum + m.gold, 0) / filteredMatches.value.length
  const yourDamage = filteredMatches.value.reduce((sum, m) => sum + m.damage, 0) / filteredMatches.value.length
  const yourParticipation = filteredMatches.value.reduce((sum, m) => sum + m.participation, 0) / filteredMatches.value.length

  // Calculate average performance (all matches)
  const avgKDAScore = matchData.value.reduce((sum, m) => sum + (m.kills + m.assists) / Math.max(1, m.deaths), 0) / matchData.value.length
  const avgCSScore = matchData.value.reduce((sum, m) => sum + m.cs, 0) / matchData.value.length
  const avgGold = matchData.value.reduce((sum, m) => sum + m.gold, 0) / matchData.value.length
  const avgDamage = matchData.value.reduce((sum, m) => sum + m.damage, 0) / matchData.value.length
  const avgParticipation = matchData.value.reduce((sum, m) => sum + m.participation, 0) / matchData.value.length

  return {
    labels: ['K/D/A', 'CS', 'Gold', 'Damage', 'Participation'],
    yourData: [
      normalizeValue(yourKDAScore * 1.15, 5),
      normalizeValue(yourCSScore * 1.1, 350),
      normalizeValue(yourGold * 1.12, 20000),
      normalizeValue(yourDamage * 1.2, 25000),
      Math.min(100, yourParticipation * 1.05)
    ],
    averageData: [
      normalizeValue(avgKDAScore * 0.85, 5),
      normalizeValue(avgCSScore * 0.9, 350),
      normalizeValue(avgGold * 0.88, 20000),
      normalizeValue(avgDamage * 0.8, 25000),
      Math.min(100, avgParticipation * 0.95)
    ]
  }
})

// Detailed stats by champion/lane/mode
const detailedStats = computed(() => {
  const statsMap = new Map()

  filteredMatches.value.forEach(match => {
    const key = `${match.champion}-${match.lane}-${match.mode}`
    if (!statsMap.has(key)) {
      statsMap.set(key, {
        champion: match.champion,
        lane: match.lane,
        mode: match.mode,
        matches: [],
      })
    }
    statsMap.get(key).matches.push(match)
  })

  return Array.from(statsMap.values()).map(stat => {
    const matches = stat.matches
    const wins = matches.filter(m => (m.kills + m.assists) > m.deaths * 2).length
    const avgKDA = matches.reduce((sum, m) => sum + (m.kills + m.assists) / Math.max(1, m.deaths), 0) / matches.length
    const avgCS = matches.reduce((sum, m) => sum + m.cs, 0) / matches.length

    return {
      champion: stat.champion,
      lane: stat.lane,
      mode: stat.mode,
      games: matches.length,
      winRate: Math.round((wins / matches.length) * 100),
      avgKDA: `${(avgKDA).toFixed(1)}`,
      avgCS: Math.round(avgCS)
    }
  }).sort((a, b) => b.games - a.games)
})

// Comparison metrics
const comparisonMetrics = ['K/D/A', 'CS', 'Gold', 'Damage', 'Participation']

const yourPerformancePercent = computed(() => {
  if (!radarData.value) return [0, 0, 0, 0, 0]
  return radarData.value.yourData
})

const averagePerformancePercent = computed(() => {
  if (!radarData.value) return [0, 0, 0, 0, 0]
  return radarData.value.averageData
})

const performanceDiff = computed(() => {
  return yourPerformancePercent.value.map((yours, idx) => {
    const avg = averagePerformancePercent.value[idx]
    return Math.round(yours - avg)
  })
})

const radarChart = ref(null)

// Initialize chart when component mounts or data changes
onMounted(() => {
  initChart()
})

watch(radarData, () => {
  initChart()
})

const initChart = () => {
  if (!radarChart.value) return

  // Destroy existing chart if it exists
  if (radarChart.value.chart) {
    radarChart.value.chart.destroy()
  }

  const ctx = radarChart.value.getContext('2d')

  // Debug: Log the data being used
  console.log('Radar Data:', radarData.value)

  const chartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: radarData.value.labels,
      datasets: [
        {
          label: 'Your Performance',
          data: radarData.value.yourData,
          borderColor: '#a855f7',
          backgroundColor: 'rgba(168, 85, 247, 0.25)',
          borderWidth: 2.5,
          pointBackgroundColor: '#a855f7',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
        },
        {
          label: 'Average Performance',
          data: radarData.value.averageData,
          borderColor: '#06b6d4',
          backgroundColor: 'rgba(6, 182, 212, 0.15)',
          borderWidth: 2.5,
          borderDash: [5, 5],
          pointBackgroundColor: '#06b6d4',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            color: '#cbd5e1',
            font: { size: 14, weight: 'bold' },
            padding: 15
          }
        }
      },
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            display: false,
            backdropColor: 'transparent'
          },
          grid: {
            color: 'rgba(99, 102, 241, 0.2)',
            lineWidth: 1.5
          },
          pointLabels: {
            display: true,
            color: '#a78bfa',
            font: {
              size: 13,
              weight: 'bold'
            },
            padding: 15,
            backdrop: {
              color: 'transparent'
            }
          }
        }
      }
    }
  })

  radarChart.value.chart = chartInstance
}
</script>

<style scoped>
.infographic-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27, #1a1f3a, #0f1628);
  padding: 40px 20px;
}

.infographic-header {
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

.infographic-header h1 {
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

/* Filter Section */
.filter-section {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: rgba(99, 102, 241, 0.1);
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
  cursor: pointer;
}

.filter-header h3 {
  margin: 0;
  color: #e2e8f0;
  font-size: 1.1rem;
  font-weight: 600;
}

.filter-toggle {
  background: none;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  transition: transform 0.3s ease;
}

.filter-toggle.collapsed {
  transform: rotate(-90deg);
}

.filter-content {
  padding: 24px;
  animation: slideDown 0.3s ease-out;
}

.filter-group {
  margin-bottom: 24px;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  display: block;
  color: #e2e8f0;
  font-weight: 600;
  margin-bottom: 12px;
  font-size: 0.95rem;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-btn {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: #cbd5e1;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.5);
}

.filter-btn.active {
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-color: #a855f7;
  color: white;
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.3);
}

.filter-btn.champion-btn.active {
  background: linear-gradient(135deg, #a855f7, #d946ef);
  box-shadow: 0 0 16px rgba(217, 70, 239, 0.4);
}

/* Stats Summary */
.stats-summary {
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
}

.stat-value {
  color: #a78bfa;
  font-size: 2rem;
  font-weight: 700;
}

/* Champion Card Layout */
.champion-radar-wrapper {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 30px;
  margin-bottom: 40px;
  align-items: start;
}

.chart-container.full-width {
  grid-column: 1 / -1;
}

.champion-card-left {
  position: sticky;
  top: 20px;
}

.champion-card {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(99, 102, 241, 0.15));
  border: 2px solid rgba(168, 85, 247, 0.4);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  animation: slideDown 0.4s ease-out;
  text-align: center;
}

.champion-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  display: block;
}

.champion-name {
  color: #e2e8f0;
  font-size: 1.8rem;
  margin: 0 0 8px 0;
  font-weight: 700;
  background: linear-gradient(135deg, #a78bfa, #d946ef);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.champion-matches {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 20px;
  font-weight: 600;
}

.quick-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.quick-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.qs-label {
  color: #94a3b8;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: 600;
}

.qs-value {
  color: #a78bfa;
  font-size: 1.3rem;
  font-weight: 700;
}

.qs-value.high {
  color: #86efac;
}

.lanes-played {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 16px;
  border-top: 1px solid rgba(99, 102, 241, 0.2);
}

.breakdown-label {
  color: #cbd5e1;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.lane-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.lane-badge {
  background: rgba(99, 102, 241, 0.2);
  color: #a78bfa;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid rgba(99, 102, 241, 0.3);
}

/* Champion Stats Card */
.champion-stats-card {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(99, 102, 241, 0.1));
  border: 2px solid rgba(168, 85, 247, 0.4);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  animation: slideDown 0.4s ease-out;
}

.champion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(168, 85, 247, 0.3);
}

.champion-header h2 {
  margin: 0;
  color: #e2e8f0;
  font-size: 1.5rem;
  font-weight: 600;
}

.champion-badge {
  background: rgba(168, 85, 247, 0.2);
  color: #a78bfa;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(168, 85, 247, 0.4);
}

.champion-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.champion-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.stat-name {
  color: #94a3b8;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 6px;
  font-weight: 600;
}

.champion-stat .stat-value {
  color: #a78bfa;
  font-size: 1.5rem;
}

.champion-stat .stat-value.high {
  color: #86efac;
}

.lanes-breakdown {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.breakdown-label {
  color: #cbd5e1;
  font-weight: 600;
  font-size: 0.9rem;
}

.lane-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.lane-badge {
  background: rgba(99, 102, 241, 0.2);
  color: #a78bfa;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid rgba(99, 102, 241, 0.3);
}

/* Chart Container */
.chart-container {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  backdrop-filter: blur(10px);
}

.champion-radar-wrapper .chart-container {
  margin-bottom: 0;
}

.champion-radar-wrapper + .stats-table-container {
  margin-top: 40px;
}

.chart-wrapper {
  position: relative;
}

.chart-wrapper h2 {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.legend-info {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #cbd5e1;
  font-weight: 500;
  font-size: 0.95rem;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  display: inline-block;
}

.legend-item.your .legend-dot {
  background: #a855f7;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.6);
}

.legend-item.average .legend-dot {
  background: #06b6d4;
  box-shadow: 0 0 8px rgba(6, 182, 212, 0.6);
}

.canvas-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 500px;
  margin: 20px auto;
}

.canvas-container canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Performance Comparison */
.performance-comparison {
  background: rgba(30, 41, 59, 0.3);
  border-top: 1px solid rgba(99, 102, 241, 0.2);
  padding: 24px;
  margin-top: 24px;
  border-radius: 12px;
}

.performance-comparison h3 {
  color: #e2e8f0;
  font-size: 1.2rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.comparison-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.metric-name {
  color: #cbd5e1;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-container {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  height: 24px;
  overflow: hidden;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.bar {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 6px;
}

.bar.your {
  background: linear-gradient(90deg, #a855f7, #d946ef);
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.4);
}

.bar.average {
  background: linear-gradient(90deg, #06b6d4, #0891b2);
  box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
}

.metric-diff {
  color: #ef4444;
  font-weight: 700;
  font-size: 1rem;
  text-align: center;
}

.metric-diff.positive {
  color: #86efac;
}

.chart-info {
  background: rgba(99, 102, 241, 0.1);
  border-left: 3px solid #a855f7;
  padding: 12px 16px;
  border-radius: 4px;
  color: #cbd5e1;
  font-size: 0.9rem;
}

.chart-info p {
  margin: 0;
}

/* Stats Table */
.stats-table-container {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  backdrop-filter: blur(10px);
}

.stats-table-container h2 {
  color: #e2e8f0;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.table-scroll {
  overflow-x: auto;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
}

.stats-table thead {
  background: rgba(99, 102, 241, 0.1);
}

.stats-table th {
  color: #a78bfa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.stats-table td {
  color: #cbd5e1;
  padding: 12px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  font-size: 0.9rem;
}

.stats-table tbody tr:hover {
  background: rgba(99, 102, 241, 0.1);
}

.stats-table td.kda {
  color: #86efac;
  font-weight: 600;
}

.stats-table td.cs {
  color: #60a5fa;
  font-weight: 600;
}

.stats-table td.winrate {
  color: #fca5a5;
  font-weight: 600;
}

.stats-table td.winrate.high {
  color: #86efac;
}

.stats-table td.games {
  color: #a78bfa;
  font-weight: 600;
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
@media (max-width: 1024px) {
  .champion-radar-wrapper {
    grid-template-columns: 1fr;
  }

  .champion-card-left {
    position: static;
  }

  .chart-container.full-width {
    grid-column: 1;
  }
}

@media (max-width: 768px) {
  .infographic-container {
    padding: 20px 10px;
  }

  .champion-radar-wrapper {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 30px;
  }

  .champion-card {
    padding: 16px;
  }

  .champion-name {
    font-size: 1.5rem;
  }

  .champion-icon {
    font-size: 3rem;
  }

  .quick-stats {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    padding: 12px;
  }

  .qs-value {
    font-size: 1.1rem;
  }

  .infographic-header h1 {
    font-size: 2rem;
  }

  .filter-buttons {
    gap: 6px;
  }

  .filter-btn {
    padding: 6px 12px;
    font-size: 0.8rem;
  }

  .filter-header {
    padding: 12px 16px;
  }

  .filter-header h3 {
    font-size: 1rem;
  }

  .filter-content {
    padding: 16px;
  }

  .champion-stats-card {
    padding: 16px;
  }

  .champion-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .champion-header h2 {
    font-size: 1.2rem;
  }

  .champion-stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .champion-stat .stat-value {
    font-size: 1.3rem;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .chart-container {
    padding: 20px;
  }

  .stats-table-container {
    padding: 20px;
  }

  .stats-table th,
  .stats-table td {
    padding: 8px;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .infographic-container {
    padding: 15px 5px;
  }

  .infographic-header h1 {
    font-size: 1.5rem;
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .filter-content {
    padding: 12px;
  }

  .filter-group {
    margin-bottom: 16px;
  }

  .filter-btn {
    padding: 5px 10px;
    font-size: 0.75rem;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .champion-stats-card {
    padding: 12px;
  }

  .champion-header {
    margin-bottom: 16px;
    padding-bottom: 12px;
  }

  .champion-header h2 {
    font-size: 1.1rem;
  }

  .champion-stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .lanes-breakdown {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-container {
    padding: 15px;
  }

  .chart-wrapper h2 {
    font-size: 1.2rem;
  }

  .stats-table-container {
    padding: 12px;
  }
}
</style>
