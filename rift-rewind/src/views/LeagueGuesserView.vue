<template>
  <div class="guesser-container">
    <div class="guesser-header">
      <div class="header-top">
        <button @click="goBack" class="back-btn">← Back</button>
        <h1>League Guesser</h1>
        <div class="spacer"></div>
      </div>
      <p class="subtitle">
        Click on the map to predict where your champion
        <span v-if="currentMetric === 'deaths'">dies</span>
        <span v-else-if="currentMetric === 'kills'">gets the most kills</span>
        <span v-else>gets the most assists</span>
        the most
      </p>
    </div>

    <!-- Champion Selector -->
    <div class="champion-selector">
      <div class="selector-label">Select Champion:</div>
      <div class="champion-buttons">
        <button v-for="champion in masteryData" :key="champion.name" @click="selectedChampion = champion.name"
          :class="{ active: selectedChampion === champion.name }" class="champion-btn">
          <img :src="getChampionIcon(champion.name)" :alt="champion.name" class="champion-icon" />
          <span>{{ champion.name }}</span>
        </button>
      </div>
    </div>

    <div class="toggle-row">
      <!-- Metric Toggle -->
      <div class="metric-toggle">
        <div class="toggle-label">Challenge:</div>
        <div class="toggle-buttons">
          <button @click="currentMetric = 'deaths'" :class="{ active: currentMetric === 'deaths' }" class="toggle-btn">
            💀 Deaths
          </button>
          <button @click="currentMetric = 'kills'" :class="{ active: currentMetric === 'kills' }" class="toggle-btn">
            ⚔️ Kills
          </button>
          <button @click="currentMetric = 'assists'" :class="{ active: currentMetric === 'assists' }"
            class="toggle-btn">
            🤝 Assists
          </button>
        </div>
      </div>

      <!-- Team Toggle -->
      <div class="metric-toggle">
        <div class="toggle-label">Side:</div>
        <div class="toggle-buttons">
          <button @click="currentTeam = 'blue'" :class="{ active: currentTeam === 'blue' }" class="toggle-btn">
            🔵 Blue
          </button>
          <button @click="currentTeam = 'red'" :class="{ active: currentTeam === 'red' }" class="toggle-btn">
            🔴 Red
          </button>
        </div>
      </div>
    </div>


    <!-- Map Container -->
    <div class="map-container">
      <div class="map-instructions">
        <p v-if="!selectedDeathLocation">
          🎯 Click on the map to guess where <b>{{ selectedChampion }} </b> 
          <span v-if="currentMetric === 'deaths'"> dies</span>
          <span v-else-if="currentMetric === 'kills'"> gets the most kills</span>
          <span v-else> gets the most assists</span>
          the most!
        </p>
        <p v-else class="result-text">
          ✓ Actual location: <strong>{{ selectedDeathLocation.location }}</strong>
          <br>
          📏 Distance: <strong>{{ distance }} pixels away</strong>
          <br>
          <span v-if="currentMetric === 'deaths'">💀 Deaths here: </span>
          <span v-else-if="currentMetric === 'kills'">⚔️ Kills here: </span>
          <span v-else>🤝 Assists here: </span>
          <strong>{{ selectedDeathLocation.count }}</strong>
        </p>
      </div>
      <div class="map-wrapper">
        <img src="/lol-map.png" alt="Summoner's Rift" class="rift-map" />
        <canvas ref="deathMapCanvas" @click="handleMapClick" class="death-heatmap"></canvas>
      </div>
      <button v-if="selectedDeathLocation" @click="resetGuess" class="reset-btn">
        Try Again
      </button>
    </div>

    <!-- Death Statistics -->
    <div class="death-stats" v-if="selectedDeathLocation && selectedChampionData">
      <div class="stat-card">
        <div class="stat-label" v-if="currentMetric === 'deaths'">💀 Total Deaths</div>
        <div class="stat-label" v-else-if="currentMetric === 'kills'">⚔️ Total Kills</div>
        <div class="stat-label" v-else>🤝 Total Assists</div>
        <div class="stat-value">{{ selectedChampionData.totalMetric }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">📍 Most Common Location</div>
        <div class="stat-value">{{ selectedChampionData.mostCommonLocation }}</div>
      </div>
    </div>

    <!-- Metrics by Location with Bars -->
    <div class="death-bars-container" v-if="selectedDeathLocation && selectedChampionData">
      <h3 class="bars-title">
        <span v-if="currentMetric === 'deaths'">🗺️ Deaths by Location</span>
        <span v-else-if="currentMetric === 'kills'">🗺️ Kills by Location</span>
        <span v-else>🗺️ Assists by Location</span>
      </h3>
      <div class="death-bars-grid">
        <div v-for="item in selectedChampionData.locationMetrics" :key="item.location" class="death-bar-item">
          <div class="bar-label">{{ item.location }}</div>
          <div class="bar-wrapper">
            <div class="bar-fill" :style="{ width: getBarWidth(item.count) + '%' }">
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import championImagesJson from '../data/championImages.json'
import kdaData from '../data/kda.json'

const router = useRouter()
const route = useRoute()

const championImagesData = ref(championImagesJson)
const kdaLocationData = ref(kdaData)
const deathMapCanvas = ref(null)
const selectedChampion = ref('Ahri')
const lastClick = ref(null)
const selectedDeathLocation = ref(null)
const distance = ref(0)
const currentMetric = ref('deaths') // 'deaths', 'kills', or 'assists'
const currentTeam = ref('blue') // 'blue' or 'red'

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

// Sample mastery data
const masteryData = ref([
  { name: 'Ahri', level: 7, points: 385000, matches: 120, winrate: 58, totalKills: 1425, totalAssists: 892, totalDeaths: 145 },
  { name: 'Lux', level: 6, points: 280000, matches: 95, winrate: 62, totalKills: 645, totalAssists: 1240, totalDeaths: 98 },
  { name: 'Zed', level: 5, points: 185000, matches: 87, winrate: 55, totalKills: 1687, totalAssists: 523, totalDeaths: 156 },
  { name: 'Yasuo', level: 6, points: 292000, matches: 110, winrate: 52, totalKills: 1532, totalAssists: 645, totalDeaths: 178 },
  { name: 'Evelynn', level: 5, points: 172000, matches: 78, winrate: 61, totalKills: 1123, totalAssists: 834, totalDeaths: 87 },
  { name: 'Akali', level: 4, points: 125000, matches: 65, winrate: 59, totalKills: 987, totalAssists: 512, totalDeaths: 112 },
  { name: 'Sylas', level: 4, points: 112000, matches: 58, winrate: 54, totalKills: 845, totalAssists: 678, totalDeaths: 134 },
  { name: 'Qiyana', level: 3, points: 78000, matches: 42, winrate: 60, totalKills: 654, totalAssists: 423, totalDeaths: 89 },
])

// Get location data based on team and metric type
const getLocationData = (metric) => {
  const teamData = kdaLocationData.value[currentTeam.value]
  if (metric === 'deaths') return teamData.deathLocationData
  if (metric === 'kills') return teamData.killLocationData
  return teamData.assistLocationData
}

// Get champion icon
const getChampionIcon = (championName) => {
  if (!championImagesData.value) return null
  const images = championImagesData.value.championImage
  return images[championName]?.championIcon || null
}

// Get selected champion data with metric info
const selectedChampionData = computed(() => {
  const champ = masteryData.value.find(c => c.name === selectedChampion.value)
  if (!champ) return null

  const locationData = getLocationData(currentMetric.value)[selectedChampion.value] || []
  const metricByLocation = {}
  let mostCommonLocation = 'Unknown'
  let maxCount = 0
  let totalMetric = 0

  locationData.forEach(loc => {
    const count = loc.count || 0
    metricByLocation[loc.location] = count
    totalMetric += count
    if (count > maxCount) {
      maxCount = count
      mostCommonLocation = loc.location
    }
  })

  // Sort location metrics from highest to lowest
  const sortedLocationMetrics = Object.entries(metricByLocation)
    .sort((a, b) => b[1] - a[1])
    .map(([location, count]) => ({ location, count }))

  return {
    ...champ,
    totalMetric,
    mostCommonLocation,
    locationMetrics: sortedLocationMetrics,
    maxMetric: maxCount,
  }
})

// Calculate bar width as percentage
const getBarWidth = (count) => {
  if (!selectedChampionData.value) return 0
  const maxMetric = selectedChampionData.value.maxMetric
  return Math.round((count / maxMetric) * 100)
}

// Draw metric heatmap
const drawDeathHeatmap = () => {
  if (!deathMapCanvas.value) return

  const canvas = deathMapCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const locationDataSet = getLocationData(currentMetric.value)[selectedChampion.value] || []

  // Find max count for normalization
  const maxCount = Math.max(...locationDataSet.map(d => d.count), 1)

  // Draw heatmap circles
  locationDataSet.forEach(location => {
    const intensity = location.count / maxCount
    const radius = 15 + intensity * 30

    // Draw gradient circle
    const gradient = ctx.createRadialGradient(location.x, location.y, 0, location.x, location.y, radius)
    gradient.addColorStop(0, `rgba(255, 0, 0, ${0.6 * intensity})`)
    gradient.addColorStop(0.5, `rgba(255, 100, 0, ${0.3 * intensity})`)
    gradient.addColorStop(1, `rgba(255, 200, 0, ${0})`)

    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(location.x, location.y, radius, 0, Math.PI * 2)
    ctx.fill()
  })
}

// Draw on canvas - shows result after click
const drawCanvas = () => {
  if (!deathMapCanvas.value) return

  const canvas = deathMapCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Always draw the heatmap
  drawDeathHeatmap()

  // If there's a click result, show it
  if (lastClick.value && selectedDeathLocation.value) {
    const clickX = lastClick.value.x
    const clickY = lastClick.value.y
    const actualX = selectedDeathLocation.value.x
    const actualY = selectedDeathLocation.value.y

    // Draw the line connecting click to actual
    ctx.strokeStyle = 'rgba(255, 200, 0, 0.8)'
    ctx.lineWidth = 2
    ctx.setLineDash([5, 5])
    ctx.beginPath()
    ctx.moveTo(clickX, clickY)
    ctx.lineTo(actualX, actualY)
    ctx.stroke()
    ctx.setLineDash([])

    // Draw user's click position (blue circle)
    ctx.fillStyle = 'rgba(100, 200, 255, 0.8)'
    ctx.beginPath()
    ctx.arc(clickX, clickY, 8, 0, Math.PI * 2)
    ctx.fill()
    ctx.strokeStyle = 'rgba(100, 200, 255, 1)'
    ctx.lineWidth = 2
    ctx.stroke()

    // Draw actual death location (red circle)
    ctx.fillStyle = 'rgba(255, 100, 100, 0.8)'
    ctx.beginPath()
    ctx.arc(actualX, actualY, 12, 0, Math.PI * 2)
    ctx.fill()
    ctx.strokeStyle = 'rgba(255, 100, 100, 1)'
    ctx.lineWidth = 2
    ctx.stroke()

    // Draw label for actual location
    ctx.fillStyle = 'white'
    ctx.font = 'bold 14px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'bottom'
    const metricValue = selectedDeathLocation.value.count || 0
    ctx.fillText(metricValue.toString(), actualX, actualY - 15)
  }
}

// Handle map click
const handleMapClick = (event) => {
  const canvas = deathMapCanvas.value
  const rect = canvas.getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const clickY = event.clientY - rect.top

  const locationDataSet = getLocationData(currentMetric.value)[selectedChampion.value] || []

  // Find the location with the MOST of the current metric
  let mostMetricLoc = null
  let maxMetric = 0

  locationDataSet.forEach(loc => {
    if (loc.count > maxMetric) {
      maxMetric = loc.count
      mostMetricLoc = loc
    }
  })

  if (mostMetricLoc) {
    // Calculate distance from click to the most common metric location
    const distToMetric = Math.sqrt((mostMetricLoc.x - clickX) ** 2 + (mostMetricLoc.y - clickY) ** 2)

    lastClick.value = { x: clickX, y: clickY }
    selectedDeathLocation.value = mostMetricLoc
    distance.value = Math.round(distToMetric)
    drawCanvas()
  }
}

// Reset click result
const resetGuess = () => {
  lastClick.value = null
  selectedDeathLocation.value = null
  distance.value = 0
  // Clear canvas
  if (deathMapCanvas.value) {
    const ctx = deathMapCanvas.value.getContext('2d')
    if (ctx) ctx.clearRect(0, 0, deathMapCanvas.value.width, deathMapCanvas.value.height)
  }
}

// Watch for champion changes and reset
import { watch } from 'vue'
watch(selectedChampion, () => {
  lastClick.value = null
  selectedDeathLocation.value = null
  distance.value = 0
  // Clear canvas when champion changes
  if (deathMapCanvas.value) {
    const ctx = deathMapCanvas.value.getContext('2d')
    if (ctx) ctx.clearRect(0, 0, deathMapCanvas.value.width, deathMapCanvas.value.height)
  }
})

// Watch for metric changes and reset
watch(currentMetric, () => {
  lastClick.value = null
  selectedDeathLocation.value = null
  distance.value = 0
  // Clear canvas when metric changes
  if (deathMapCanvas.value) {
    const ctx = deathMapCanvas.value.getContext('2d')
    if (ctx) ctx.clearRect(0, 0, deathMapCanvas.value.width, deathMapCanvas.value.height)
  }
})

// Watch for team changes and reset
watch(currentTeam, () => {
  lastClick.value = null
  selectedDeathLocation.value = null
  distance.value = 0
  // Clear canvas when team changes
  if (deathMapCanvas.value) {
    const ctx = deathMapCanvas.value.getContext('2d')
    if (ctx) ctx.clearRect(0, 0, deathMapCanvas.value.width, deathMapCanvas.value.height)
  }
})

// Initialize canvas on mount
onMounted(() => {
  // Set canvas size to match map
  const mapImg = document.querySelector('.rift-map')
  if (mapImg && deathMapCanvas.value) {
    mapImg.onload = () => {
      deathMapCanvas.value.width = mapImg.width
      deathMapCanvas.value.height = mapImg.height
    }
  }

  // Set canvas size after a delay
  setTimeout(() => {
    const mapImg = document.querySelector('.rift-map')
    if (mapImg && deathMapCanvas.value) {
      deathMapCanvas.value.width = mapImg.width
      deathMapCanvas.value.height = mapImg.height
    }
  }, 500)
})
</script>

<style scoped>
.guesser-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27, #1a1f3a, #0f1628);
  padding: 40px 20px;
}

.guesser-header {
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

.guesser-header h1 {
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

.champion-selector {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
}

.selector-label {
  color: #cbd5e1;
  font-weight: bold;
  margin-bottom: 15px;
  font-size: 1rem;
}

.champion-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.champion-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.champion-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.4);
}

.champion-btn.active {
  background: linear-gradient(135deg, #a855f7, #ec4899);
  border-color: #a855f7;
  color: #fff;
}

.champion-icon {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  object-fit: cover;
}

.map-container {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.map-instructions {
  text-align: center;
  margin-bottom: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.map-instructions p {
  margin: 0;
  color: #cbd5e1;
  font-size: 1rem;
}

.result-text {
  color: #a8e6cf !important;
  line-height: 1.6;
}

.reset-btn {
  display: block;
  margin: 15px auto 0;
  padding: 10px 20px;
  background: linear-gradient(135deg, #a855f7, #ec4899);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
}

.map-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.rift-map {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}

.death-heatmap {
  position: absolute;
  top: 0;
  left: 0;
  cursor: crosshair;
  border-radius: 8px;
}

.death-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
  animation: slideDown 0.6s ease-out 0.2s both;
}

.stat-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: default;
}

.stat-card:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(99, 102, 241, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

.stat-label {
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  display: block;
  font-weight: 600;
}

.stat-value {
  color: #a78bfa;
  font-size: 2rem;
  font-weight: 700;
  display: block;
  margin-bottom: 0;
}

.death-bars-container {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 40px;
  backdrop-filter: blur(10px);
  animation: slideDown 0.6s ease-out 0.3s both;
}

.bars-title {
  color: #e2e8f0;
  font-size: 1.3rem;
  margin: 0 0 24px 0;
  font-weight: 600;
}

.death-bars-grid {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.death-bar-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-label {
  color: #cbd5e1;
  font-size: 0.95rem;
  font-weight: 500;
}

.bar-wrapper {
  height: 32px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #a855f7, #ec4899);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 12px;
  min-width: 30px;
  animation: expandBar 0.6s ease-out;
  position: relative;
  transition: all 0.3s ease;
}

.bar-fill:hover {
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
  filter: brightness(1.1);
}

.bar-value {
  color: #fff;
  font-weight: 700;
  font-size: 0.9rem;
  white-space: nowrap;
}

.toggle-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3em; /* space between the two toggle groups */
}


.metric-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 30px;
  animation: slideDown 0.6s ease-out;
}

.toggle-label {
  color: #94a3b8;
  font-size: 0.95rem;
  font-weight: 600;
}

.toggle-buttons {
  display: flex;
  gap: 8px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  padding: 6px;
  backdrop-filter: blur(10px);
}

.toggle-btn {
  padding: 8px 16px;
  background: transparent;
  border: 2px solid transparent;
  color: #cbd5e1;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background: rgba(99, 102, 241, 0.1);
  color: #e2e8f0;
}

.toggle-btn.active {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(236, 72, 153, 0.3));
  border-color: rgba(168, 85, 247, 0.5);
  color: #e2e8f0;
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.2);
}

@keyframes expandBar {
  from {
    width: 0;
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

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
</style>
