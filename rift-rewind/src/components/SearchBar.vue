<template>
  <div class="search-bar-container">
    <form @submit.prevent="handleSearch" class="search-form">
      <div class="input-fields">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Enter your Riot ID (e.g., PlayerName#NA1)"
          @keyup.enter="handleSearch"
        />
        <select v-model="selectedRegion" class="region-select">
          <option value="">Select Region</option>
          <option v-for="(region, code) in regionGroups" :key="code" :value="region">
            {{ code }}
          </option>
        </select>
      </div>
      <button class="search-btn" type="submit">
        <span class="search-icon">Rewind</span>
      </button>
    </form>
    <p v-if="errorMessage" class="error-text mt-2">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchQuery = ref('Garbadger#6969')
const selectedRegion = ref('')
const errorMessage = ref('')

const regionGroups = {
  'NA': 'AMERICAS',
  'EU': 'EUROPE',
  'ASIA': 'ASIA'
}

const emit = defineEmits(['search'])

const handleSearch = () => {
  errorMessage.value = ''

  if (!searchQuery.value.trim()) {
    errorMessage.value = 'Please enter a Riot ID'
    return
  }

  if (!selectedRegion.value) {
    errorMessage.value = 'Please select a region'
    return
  }

  emit('search', { riotId: searchQuery.value, region: selectedRegion.value })
  searchQuery.value = ''
  selectedRegion.value = ''
}
</script>

<style scoped>
.search-bar-container {
  width: 100%;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 0;
  align-items: flex-start;
}

.input-fields {
  display: flex;
  gap: 12px;
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.98);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  width: 100%;
  margin-bottom: 24px;
}

.input-fields:focus-within {
  box-shadow:
    0 15px 40px rgba(25, 118, 210, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  transform: translateY(-3px);
}

.search-input {
  border: none;
  padding: 14px 18px;
  font-size: 15px;
  background-color: transparent;
  color: #1a1a1a;
  transition: all 0.3s ease;
  flex: 1;
  font-weight: 500;
  letter-spacing: 0.2px;
  min-width: 0;
}

.search-input::placeholder {
  color: #9e9e9e;
  font-weight: 400;
}

.search-input:focus {
  outline: none;
  color: #1a1a1a;
}

.region-select {
  border: none;
  border-left: 1px solid #e0e0e0;
  padding: 14px 16px;
  font-size: 15px;
  background-color: transparent;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 0.2px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/csvg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 20px;
  padding-right: 32px;
  min-width: 140px;
}

.region-select:focus {
  outline: none;
  color: #1a1a1a;
}

.region-select option {
  color: #1a1a1a;
  background-color: #fff;
}

.search-btn {
  border: none;
  padding: 11px 48px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
  color: white;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 18px;
  letter-spacing: 0.5px;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
  border-radius: 14px;
  box-shadow:
    0 8px 25px rgba(99, 102, 241, 0.3),
    0 0 20px rgba(168, 85, 247, 0.15);
  width: auto;
  margin: 0 auto;
  text-transform: uppercase;
  min-width: 180px;
}

.search-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  transition: left 0.6s ease;
}

.search-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 14px;
  padding: 2px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.search-btn:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #d946ef 100%);
  transform: translateY(-4px);
  box-shadow:
    0 12px 35px rgba(124, 58, 237, 0.4),
    0 0 30px rgba(217, 70, 239, 0.25);
  letter-spacing: 0.8px;
}

.search-btn:hover::before {
  left: 100%;
}

.search-btn:hover::after {
  opacity: 1;
}

.search-btn:active {
  transform: translateY(-1px);
  box-shadow:
    0 4px 15px rgba(124, 58, 237, 0.3),
    0 0 15px rgba(168, 85, 247, 0.15);
}

.search-icon {
  font-size: 20px;
  font-weight: 800;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
}

.search-btn:hover .search-icon {
  transform: scale(1.1);
  letter-spacing: 1px;
}

.error-text {
  color: #ef5350;
  font-size: 13px;
  font-weight: 500;
  margin-top: 10px;
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

@media (max-width: 576px) {
  .input-fields {
    flex-direction: column;
    gap: 0;
    margin-bottom: 18px;
  }

  .search-input {
    font-size: 14px;
    padding: 12px 14px;
  }

  .region-select {
    border-left: none;
    border-top: 1px solid #e0e0e0;
    font-size: 14px;
    padding: 12px 14px;
    padding-right: 28px;
    min-width: auto;
  }

  .search-btn {
    padding: 10px 32px;
    font-size: 16px;
    min-width: 160px;
  }

  .search-icon {
    font-size: 18px;
  }
}
</style>
