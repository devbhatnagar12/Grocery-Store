<template>
<NavbarComponent/>
<RouterView/>
</template>

<script setup>
import { RouterView } from 'vue-router';
import NavbarComponent from './components/NavbarComponent.vue';
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
  
}
*{
  background-color: beige;
}
</style>
