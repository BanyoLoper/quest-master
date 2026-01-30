<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const quests = ref([])
const newQuest = ref({ title: '', description: '', points_reward: 10 })

// Obtener misiones
const fetchQuests = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/quests/')
  quests.value = response.data
}

// Agregar misión
const addQuest = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/quests/', newQuest.value)
    newQuest.value = { title: '', description: '', points_reward: 10 } // Limpiar form
    fetchQuests() // Recargar lista
  } catch (error) {
    console.error("Error al crear la misión", error)
  }
}

onMounted(fetchQuests)
</script>

<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">Quest Master Admin</h1>
    
    <div class="mb-8 p-4 border rounded shadow-sm">
      <h2 class="font-bold">Crear Nueva Misión</h2>
      <input v-model="newQuest.title" placeholder="Título" class="border p-2 mr-2" />
      <input v-model="newQuest.description" placeholder="Descripción" class="border p-2 mr-2" />
      <input v-model="newQuest.points_reward" type="number" class="border p-2 mr-2" />
      <button @click="addQuest" class="bg-blue-500 text-white px-4 py-2 rounded">Agregar</button>
    </div>

    <ul>
      <li v-for="quest in quests" :key="quest.id" class="mb-2 p-2 bg-gray-100 rounded">
        <strong>{{ quest.title }}</strong> - {{ quest.points_reward }} XP
      </li>
    </ul>
  </div>
</template>