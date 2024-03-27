<template>
    <div class="input-group">
      <input type="text" class="form-control" v-model="searchQuery" placeholder="Search...">
      <div class="input-group-append">
        <button class="btn btn-outline-secondary" @click="performSearch">Search</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from 'vue';
  
  const emits = defineEmits(['search']);
  const searchQuery = ref('');
  
  const performSearch = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/section?name=${searchQuery.value}`, {
      });
      console.log("response", response)

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("ddddd", data)
      
      // Emit the search event to the parent component with the filtered data
      emits('search', data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  </script>
  
  <style scoped>

  </style>
  