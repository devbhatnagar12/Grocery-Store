<template>
    <component :is="home"></component>

</template>

<script setup>
import { ref, computed } from 'vue';
import { getRole } from '../helpers/authHelper'
import HomeComponentManager from '../components/manager/HomeComponent'
import HomeComponentUser from '../components/user/HomeComponent'
import HomeComponentAdmin from '../components/admin/HomeComponent'


const role = ref(getRole())

const home = computed(() => {
    switch(role.value) {
        case 'manager':
            return HomeComponentManager;
        case 'user':
            return HomeComponentUser;
        case 'admin':
            return HomeComponentAdmin;
        default:
            return HomeComponentUser; 
    }
});

</script>