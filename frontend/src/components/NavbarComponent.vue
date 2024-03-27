<template>
    <component :is="navbar"></component>
</template>

<script setup>
import { ref, computed } from 'vue';
import ManagerNavbar from './manager/ManagerNavbar.vue';
import UserNavbar from './user/UserNavbar.vue';
import AdminNavbar from './admin/AdminNavbar.vue';

import { getRole } from '../helpers/authHelper';

const role = ref(getRole());
console.log("navbar role: " + role.value);


const navbar = computed(() => {
    switch(role.value) {
        case 'manager':
            return ManagerNavbar;
        case 'user':
            return UserNavbar;
        case 'admin':
            return AdminNavbar;
        default:
            return {};
    }
});

</script>