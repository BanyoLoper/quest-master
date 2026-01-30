<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- ESTADOS DE AUTENTICACIÓN ---
const isAuthenticated = ref(false)
const isLoginMode = ref(true) // Cambia entre Login y Registro
const authData = ref({
  username: '',
  password: '',
  email: '' // Solo se usa en registro
})

// --- ESTADOS DEL JUEGO ---
const quests = ref([])
const player = ref({ username: '', xp: 0, achievements: [] })
const newQuest = ref({ title: '', description: '', points_reward: 10 })

const API_URL = 'http://127.0.0.1:8000/api/'

// --- LÓGICA DE AUTENTICACIÓN ---
const handleAuth = async () => {
  try {
    const endpoint = isLoginMode.value ? 'token/' : 'register/'
    const payload = isLoginMode.value 
      ? { username: authData.value.username, password: authData.value.password }
      : authData.value

    const response = await axios.post(`${API_URL}${endpoint}`, payload)

    if (isLoginMode.value) {
      // Guardar tokens y configurar Axios
      localStorage.setItem('accessToken', response.data.access)
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      isAuthenticated.value = true
      fetchData()
    } else {
      alert("¡Héroe registrado! Ahora inicia sesión.")
      isLoginMode.value = true // Cambiamos a login tras registrarse
    }
  } catch (error) {
    console.error("Auth error:", error)
    alert("Error: " + (error.response?.data?.detail || "Revisa tus datos"))
  }
}

// --- LÓGICA DE DATOS ---
const fetchData = async () => {
  if (!isAuthenticated.value) return
  try {
    const qRes = await axios.get(`${API_URL}quests/`)
    quests.value = qRes.data
    // Aquí podrías cargar también el perfil del usuario actual
  } catch (err) {
    console.error("Error cargando datos:", err)
  }
}

const createQuest = async () => {
  try {
    await axios.post(`${API_URL}quests/`, newQuest.value)
    newQuest.value = { title: '', description: '', points_reward: 10 }
    fetchData()
  } catch (err) {
    alert("No tienes permisos o faltan datos")
  }
}

// Al cargar, verificamos si ya había un token
onMounted(() => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    isAuthenticated.value = true
    fetchData()
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white font-sans">
    
    <div v-if="!isAuthenticated" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md">
      <div class="bg-gray-800 p-8 rounded-2xl border border-gray-700 w-full max-w-md shadow-2xl mx-4">
        <h2 class="text-3xl font-black text-yellow-400 mb-6 uppercase tracking-tighter italic text-center">
          {{ isLoginMode ? 'Player Login' : 'New Hero Registry' }}
        </h2>
        
        <div class="space-y-4">
          <div>
            <label class="text-xs text-gray-400 uppercase font-bold">Username</label>
            <input v-model="authData.username" type="text" class="w-full bg-gray-700 p-3 rounded border-none outline-none focus:ring-2 focus:ring-yellow-500">
          </div>
          
          <div v-if="!isLoginMode">
            <label class="text-xs text-gray-400 uppercase font-bold">Email</label>
            <input v-model="authData.email" type="email" class="w-full bg-gray-700 p-3 rounded border-none outline-none focus:ring-2 focus:ring-yellow-500">
          </div>

          <div>
            <label class="text-xs text-gray-400 uppercase font-bold">Password</label>
            <input v-model="authData.password" type="password" class="w-full bg-gray-700 p-3 rounded border-none outline-none focus:ring-2 focus:ring-yellow-500">
          </div>
          
          <button @click="handleAuth" class="w-full bg-yellow-500 text-gray-900 font-black py-4 rounded-xl hover:bg-yellow-400 transition-all transform active:scale-95">
            {{ isLoginMode ? 'START ADVENTURE' : 'SIGN UP NOW' }}
          </button>
          
          <p @click="isLoginMode = !isLoginMode" class="text-center text-sm text-gray-400 cursor-pointer hover:text-yellow-400 transition-colors">
            {{ isLoginMode ? "¿No tienes cuenta? Regístrate aquí" : "¿Ya eres miembro? Inicia sesión" }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="isAuthenticated" class="p-4 md:p-8 max-w-7xl mx-auto">
      <header class="flex justify-between items-center mb-12 border-b border-gray-700 pb-6">
        <div>
          <h1 class="text-4xl font-black tracking-tighter text-yellow-400 italic">QUEST MASTER <span class="text-white text-xs font-light not-italic ml-2">v1.0</span></h1>
          <p class="text-gray-500 text-xs tracking-widest uppercase">Development Environment</p>
        </div>
        <div class="text-right">
          <p class="font-bold text-xl text-white">{{ player.username || 'Admin_User' }}</p>
          <p class="text-blue-400 text-sm font-mono tracking-tighter">Level Explorer ({{ player.xp }} XP)</p>
          <button @click="isAuthenticated = false; localStorage.clear()" class="text-[10px] text-red-500 hover:underline">LOGOUT</button>
        </div>
      </header>

      <main class="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <section class="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl self-start">
          <h2 class="text-xl font-bold mb-6 flex items-center">
            <span class="bg-yellow-500 w-2 h-6 mr-3"></span> FORGE NEW QUEST
          </h2>
          
          <div class="space-y-5">
            <div>
              <label class="block text-[10px] uppercase text-gray-400 mb-1 font-bold">Quest Title</label>
              <input v-model="newQuest.title" type="text" placeholder="Ex: Kill the Python Bug" class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-yellow-500 outline-none transition-all">
            </div>
            <div>
              <label class="block text-[10px] uppercase text-gray-400 mb-1 font-bold">Objective Description</label>
              <textarea v-model="newQuest.description" placeholder="Describe the mission goals..." class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 h-28 outline-none focus:ring-2 focus:ring-yellow-500 transition-all"></textarea>
            </div>
            <div>
              <label class="block text-[10px] uppercase text-gray-400 mb-1 font-bold">XP Reward</label>
              <input v-model="newQuest.points_reward" type="number" class="w-full md:w-1/3 bg-gray-900 border border-gray-700 rounded-lg p-3 outline-none focus:ring-2 focus:ring-yellow-500">
            </div>
            <button @click="createQuest" class="w-full bg-yellow-500 hover:bg-yellow-400 text-gray-900 font-black py-4 rounded-xl transition-all shadow-lg shadow-yellow-500/10">
              DEPLOY TO WORLD
            </button>
          </div>
        </section>

        <section>
          <h2 class="text-xl font-bold mb-6 flex items-center">
             <span class="bg-blue-500 w-2 h-6 mr-3"></span> ACTIVE WORLD EVENTS
          </h2>
          <div class="space-y-4">
            <div v-for="q in quests" :key="q.id" class="bg-gray-800 p-5 rounded-xl border border-gray-700 flex justify-between items-center hover:border-blue-500 transition-all group">
              <div>
                <h3 class="font-bold text-lg group-hover:text-blue-400 transition-colors">{{ q.title }}</h3>
                <p class="text-gray-400 text-sm italic">{{ q.description }}</p>
              </div>
              <div class="text-right">
                <span class="text-blue-400 font-black text-2xl">+{{ q.points_reward }}</span>
                <p class="text-[10px] text-gray-500 uppercase font-bold">XP Points</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer class="mt-12 p-8 bg-black rounded-3xl border border-gray-800">
        <h3 class="text-xs font-black text-gray-500 mb-6 uppercase tracking-[0.3em] text-center">Unlocked Achievement Badges</h3>
        <div class="flex flex-wrap justify-center gap-6">
          <div v-if="player.achievements.length === 0" class="text-gray-700 text-sm italic">No badges earned yet... keep grinding.</div>
          <div v-for="ach in player.achievements" :key="ach.id" class="group relative">
            <div class="text-4xl bg-gray-900 p-4 rounded-full border border-yellow-600/30 shadow-[0_0_20px_rgba(234,179,8,0.1)] group-hover:scale-110 transition-transform cursor-help">
              {{ ach.icon }}
            </div>
            <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-yellow-500 text-gray-900 text-[10px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              {{ ach.name }}
            </div>
          </div>
        </div>
      </footer>
    </div>

  </div>
</template>

<style scoped>
/* Transiciones suaves para el modal */
.v-enter-active, .v-leave-active {
  transition: opacity 0.5s ease;
}
.v-enter-from, .v-leave-to {
  opacity: 0;
}
</style>