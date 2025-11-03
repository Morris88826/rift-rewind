<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <div class="header-top">
        <button @click="goBack" class="back-btn">← Back</button>
        <h1>Match Calendar</h1>
        <div class="spacer"></div>
      </div>
      <p class="subtitle">View your match history by date</p>
    </div>

    <!-- Month Navigation -->
    <div class="month-navigation">
      <button @click="previousMonth" class="nav-btn" :disabled="currentMonth === 0" aria-label="Previous month">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>

      <div class="current-month">
        <div class="month-selector">
          <select v-model.number="selectedMonth" @change="updateMonth" class="selector-dropdown">
            <option v-for="(month, index) in monthNames" :key="index" :value="index">
              {{ month }}
            </option>
          </select>
          <div class="year-display">{{ currentYearValue }}</div>
        </div>
        <button @click="goToToday" class="today-btn" title="Go to today">Today</button>
      </div>

      <button @click="nextMonth" class="nav-btn" :disabled="currentMonth === 11" aria-label="Next month">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>

    <!-- Days of Week Header -->
    <div class="days-header">
      <div v-for="day in daysOfWeek" :key="day" class="day-label">
        {{ day }}
      </div>
    </div>

    <!-- Calendar Grid -->
    <div class="calendar-grid">
      <!-- Empty cells for days before month starts -->
      <div
        v-for="n in firstDayOfMonth"
        :key="`empty-${n}`"
        class="calendar-cell empty"
      ></div>

      <!-- Calendar days -->
      <button
        v-for="day in daysInMonth"
        :key="day"
        @click="selectDay(day)"
        class="calendar-cell day"
        :class="{
          'has-matches': hasMatches(day),
          active: selectedDay === day,
          today: isToday(day),
        }"
        :aria-label="`${day} ${currentMonth + 1}/${currentYear}${hasMatches(day) ? ' - has matches' : ''}`"
      >
        <div class="day-number">{{ day }}</div>
        <div v-if="hasMatches(day)" class="match-indicator">
          <span class="dot"></span>
        </div>
      </button>
    </div>

    <!-- Legend -->
    <div class="calendar-legend">
      <div class="legend-item">
        <span class="legend-dot"></span>
        <span>Has matches</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot today"></span>
        <span>Today</span>
      </div>
    </div>

    <!-- Match Story Modal -->
    <Transition name="modal-fade">
      <MatchStoryModal
        v-if="selectedDay"
        :day="selectedDay"
        :month="currentMonth + 1"
        :year="currentYear"
        :matches="getMatchesForDay(selectedDay)"
        @close="selectedDay = null"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MatchStoryModal from '../components/MatchStoryModal.vue'

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

const selectedDay = ref(null)
const currentDate = ref(new Date())

const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

const selectedMonth = ref(currentDate.value.getMonth())
const selectedYear = ref(currentDate.value.getFullYear())

const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())

const currentYearValue = computed(() => {
  const today = new Date()
  return today.getFullYear()
})

const availableYears = computed(() => {
  return [currentYearValue.value]
})

const currentMonthYear = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
})

const firstDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1).getDay()
})

// Sync selectedMonth and selectedYear when calendar changes
watch([currentMonth, currentYear], () => {
  selectedMonth.value = currentMonth.value
  selectedYear.value = currentYear.value
})

// Sample match history data
const matchHistoryData = ref({
  // Format: 'YYYY-MM-DD': [matches]
  '2025-11-03': [
    {
      id: 1,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Victory',
      kills: 12,
      deaths: 2,
      assists: 8,
      cs: 287,
      duration: '35m 42s',
      lp: '+21',
      timestamp: '2025-11-03T18:30:00',
    },
    {
      id: 2,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Defeat',
      kills: 7,
      deaths: 5,
      assists: 14,
      cs: 256,
      duration: '28m 15s',
      lp: '-15',
      timestamp: '2025-11-03T19:15:00',
    },
  ],
  '2025-11-02': [
    {
      id: 3,
      champion: 'Lux',
      role: 'Support',
      result: 'Victory',
      kills: 3,
      deaths: 1,
      assists: 21,
      cs: 45,
      duration: '32m 10s',
      lp: '+18',
      timestamp: '2025-11-02T20:00:00',
    },
  ],
  '2025-11-01': [
    {
      id: 4,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Victory',
      kills: 15,
      deaths: 3,
      assists: 12,
      cs: 312,
      duration: '38m 25s',
      lp: '+24',
      timestamp: '2025-11-01T17:45:00',
    },
    {
      id: 5,
      champion: 'Lux',
      role: 'Support',
      result: 'Victory',
      kills: 2,
      deaths: 2,
      assists: 18,
      cs: 52,
      duration: '33m 40s',
      lp: '+19',
      timestamp: '2025-11-01T18:50:00',
    },
    {
      id: 6,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Defeat',
      kills: 8,
      deaths: 6,
      assists: 10,
      cs: 278,
      duration: '30m 05s',
      lp: '-18',
      timestamp: '2025-11-01T20:15:00',
    },
  ],
  '2025-10-31': [
    {
      id: 7,
      champion: 'Zed',
      role: 'Mid',
      result: 'Victory',
      kills: 18,
      deaths: 2,
      assists: 5,
      cs: 334,
      duration: '36m 20s',
      lp: '+26',
      timestamp: '2025-10-31T19:00:00',
    },
  ],
  '2025-10-28': [
    {
      id: 8,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Victory',
      kills: 10,
      deaths: 4,
      assists: 9,
      cs: 295,
      duration: '34m 15s',
      lp: '+22',
      timestamp: '2025-10-28T18:30:00',
    },
  ],
  '2025-10-25': [
    {
      id: 9,
      champion: 'Lux',
      role: 'Support',
      result: 'Victory',
      kills: 4,
      deaths: 1,
      assists: 25,
      cs: 58,
      duration: '31m 50s',
      lp: '+20',
      timestamp: '2025-10-25T17:20:00',
    },
    {
      id: 10,
      champion: 'Ahri',
      role: 'Mid',
      result: 'Victory',
      kills: 11,
      deaths: 3,
      assists: 11,
      cs: 305,
      duration: '37m 05s',
      lp: '+23',
      timestamp: '2025-10-25T18:45:00',
    },
  ],
})

const previousMonth = () => {
  // Only allow navigation within current year
  if (currentMonth.value > 0) {
    currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
  }
}

const nextMonth = () => {
  // Only allow navigation within current year
  if (currentMonth.value < 11) {
    currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  }
}

const updateMonth = () => {
  // Always use current year since rewind is yearly
  currentDate.value = new Date(currentYearValue.value, selectedMonth.value, 1)
}

const goToToday = () => {
  const today = new Date()
  // Only navigate to today if it's in the current year
  if (today.getFullYear() === currentYearValue.value) {
    selectedMonth.value = today.getMonth()
    currentDate.value = new Date(today.getFullYear(), today.getMonth(), 1)
  }
}

const selectDay = (day) => {
  selectedDay.value = day
}

const hasMatches = (day) => {
  const dateStr = formatDateString(day)
  return matchHistoryData.value[dateStr] && matchHistoryData.value[dateStr].length > 0
}

const getMatchesForDay = (day) => {
  const dateStr = formatDateString(day)
  return matchHistoryData.value[dateStr] || []
}

const isToday = (day) => {
  const today = new Date()
  return (
    day === today.getDate() &&
    currentMonth.value === today.getMonth() &&
    currentYear.value === today.getFullYear()
  )
}

const formatDateString = (day) => {
  const month = String(currentMonth.value + 1).padStart(2, '0')
  const dayStr = String(day).padStart(2, '0')
  return `${currentYear.value}-${month}-${dayStr}`
}
</script>

<style scoped>
.calendar-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27, #1a1f3a, #0f1628);
  padding: 40px 20px;
}

.calendar-header {
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

.back-btn:active {
  transform: translateX(-2px);
}

.spacer {
  width: 60px;
}

.calendar-header h1 {
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

/* Month Navigation */
.month-navigation {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 30px;
}

.nav-btn {
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #e2e8f0;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: rgba(99, 102, 241, 0.4);
  border-color: rgba(99, 102, 241, 0.6);
  transform: scale(1.05);
}

.nav-btn:active {
  transform: scale(0.95);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.nav-btn:disabled:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.4);
  transform: scale(1);
}

.current-month {
  display: flex;
  align-items: center;
  gap: 12px;
}

.month-selector {
  display: flex;
  gap: 10px;
  align-items: center;
}

.selector-dropdown {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #e2e8f0;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 110px;
}

.year-display {
  color: #e2e8f0;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 12px;
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.4);
  border-radius: 8px;
  min-width: 60px;
  text-align: center;
}

.selector-dropdown:hover {
  background: rgba(30, 41, 59, 1);
  border-color: rgba(99, 102, 241, 0.6);
}

.selector-dropdown:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(30, 41, 59, 1);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.selector-dropdown option {
  background: #1a1f3a;
  color: #e2e8f0;
  padding: 8px;
}

.today-btn {
  background: rgba(168, 85, 247, 0.2);
  border: 1px solid rgba(168, 85, 247, 0.4);
  color: #e2e8f0;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s;
  white-space: nowrap;
}

.today-btn:hover {
  background: rgba(168, 85, 247, 0.3);
  border-color: rgba(168, 85, 247, 0.6);
}

.today-btn:active {
  transform: scale(0.95);
}

/* Days Header */
.days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 12px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.day-label {
  text-align: center;
  color: #94a3b8;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Calendar Grid */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  max-width: 600px;
  margin: 0 auto 30px;
  padding: 0 20px;
  box-sizing: border-box;
}

.calendar-cell {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border-radius: 12px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  font-size: 0.9rem;
  font-weight: 500;
}

.calendar-cell.empty {
  cursor: default;
  background: transparent;
  border: none;
}

.calendar-cell.day {
  color: #cbd5e1;
}

.calendar-cell.day:hover:not(.empty) {
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.5);
  transform: translateY(-2px);
}

.calendar-cell.day.has-matches {
  background: rgba(99, 102, 241, 0.15);
  border-color: rgba(168, 85, 247, 0.5);
}

.calendar-cell.day.has-matches:hover {
  background: rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.7);
}

.calendar-cell.day.today {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.2));
  border: 2px solid rgba(168, 85, 247, 0.6);
  font-weight: 700;
}

.calendar-cell.day.today .day-number {
  color: #a78bfa;
}

.calendar-cell.day.active {
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-color: #a855f7;
  color: white;
  box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
}

.calendar-cell.day.active .day-number {
  color: white;
}

.day-number {
  font-size: 1.2rem;
  font-weight: 600;
}

.match-indicator {
  display: flex;
  gap: 3px;
}

.match-indicator .dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #a855f7;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Legend */
.calendar-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 20px;
  margin-bottom: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #cbd5e1;
  font-size: 0.875rem;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #a855f7;
}

.legend-dot.today {
  border: 2px solid #a855f7;
  background: transparent;
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

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .calendar-container {
    padding: 20px 10px;
  }

  .calendar-header h1 {
    font-size: 2rem;
  }

  .month-navigation {
    gap: 12px;
  }

  .month-selector {
    gap: 6px;
  }

  .selector-dropdown {
    min-width: 90px;
    padding: 6px 10px;
    font-size: 0.85rem;
  }

  .year-display {
    min-width: 50px;
    padding: 6px 10px;
    font-size: 0.85rem;
  }

  .today-btn {
    padding: 6px 12px;
    font-size: 0.75rem;
  }

  .days-header,
  .calendar-grid {
    gap: 6px;
    max-width: 100%;
    padding: 0 10px;
  }

  .calendar-cell {
    font-size: 0.8rem;
  }

  .calendar-legend {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 500px) {
  .calendar-container {
    padding: 20px 5px;
  }

  .days-header,
  .calendar-grid {
    max-width: calc(100vw - 10px);
  }
}
</style>
