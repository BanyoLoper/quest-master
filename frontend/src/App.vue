<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const quests = ref([])
const player = ref({ username: '', xp: 0, achievements: [] })
const newQuest = ref({ title: '', description: '', points_reward: 10 })

const API_URL = 'http://127.0.0.1:8000/api/'

const fetchData = async () => {
  try {
    const qRes = await axios.get(`${API_URL}quests/`)
    quests.value = qRes.data
    // Aquí podrías obtener el perfil del jugador logueado
    // Por ahora simularemos el ID 1 para el ejemplo
  } catch (err) { console.error(err) }
}

const createQuest = async () => {
  await axios.post(`${API_URL}quests/`, newQuest.value)
  newQuest.value = { title: '', description: '', points_reward: 10 }
  fetchData()
}

onMounted(fetchData)
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white p-8 font-sans">
    <header class="flex justify-between items-center mb-12 border-b border-gray-700 pb-4">
      <h1 class="text-3xl font-black tracking-tighter text-yellow-400">QUEST MASTER <span class="text-white text-sm font-light">v1.0</span></h1>
      <div class="text-right">
        <p class="font-bold text-xl">{{ player.username || 'Admin_User' }}</p>
        <p class="text-blue-400 text-sm">Level Explorer ({{ player.xp }} XP)</p>
      </div>
    </header>

    <main class="grid grid-cols-1 md:grid-cols-2 gap-10">
      <section class="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-2xl">
        <h2 class="text-xl font-bold mb-6 flex items-center">
          <span class="bg-yellow-500 w-2 h-6 mr-3"></span> Forge New Quest
        </h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-xs uppercase text-gray-400 mb-1">Quest Title</label>
            <input v-model="newQuest.title" type="text" class="w-full bg-gray-700 border-none rounded p-3 focus:ring-2 focus:ring-yellow-500 outline-none">
          </div>
          <div>
            <label class="block text-xs uppercase text-gray-400 mb-1">Objective Description</label>
            <textarea v-model="newQuest.description" class="w-full bg-gray-700 border-none rounded p-3 h-24 outline-none"></textarea>
          </div>
          <div>
            <label class="block text-xs uppercase text-gray-400 mb-1">XP Reward</label>
            <input v-model="newQuest.points_reward" type="number" class="w-1/3 bg-gray-700 border-none rounded p-3 outline-none">
          </div>
          <button @click="createQuest" class="w-full bg-yellow-500 hover:bg-yellow-400 text-gray-900 font-bold py-3 rounded-lg transition-all transform active:scale-95">
            DEPLOY QUEST
          </button>
        </div>
      </section>

      <section>
        <h2 class="text-xl font-bold mb-6">Active World Events</h2>
        <div class="grid gap-4">
          <div v-for="q in quests" :key="q.id" class="bg-gray-800 p-4 rounded-lg border-l-4 border-blue-500 flex justify-between items-center hover:bg-gray-750 transition-colors">
            <div>
              <h3 class="font-bold text-lg">{{ q.title }}</h3>
              <p class="text-gray-400 text-sm">{{ q.description }}</p>
            </div>
            <div class="text-right">
              <span class="text-blue-400 font-mono text-xl">+{{ q.points_reward }}</span>
              <p class="text-[10px] text-gray-500 uppercase">Experience</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="mt-12 p-6 bg-black rounded-t-2xl">
      <h3 class="text-sm font-bold text-gray-500 mb-4 uppercase tracking-widest">Unlocked Badges</h3>
      <div class="flex gap-4">
        <div v-for="ach in player.achievements" :key="ach.id" class="group relative">
          <div class="text-4xl bg-gray-800 p-3 rounded-full border border-yellow-600 shadow-[0_0_15px_rgba(234,179,8,0.2)]">
            {{ ach.icon }}
          </div>
          <span class="absolute -bottom-8 left-1/2 -translate-x-1/2 text-[10px] whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
            {{ ach.name }}
          </span>
        </div>
      </div>
    </footer>
  </div>
</template>