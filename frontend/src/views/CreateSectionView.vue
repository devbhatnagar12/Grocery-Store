<template>
    <div class="container">
        <form @submit.prevent="createSection" class="mt-5">
            <div class="mb-3">
                <label for="section-name" class="form-label">Section Name:</label>
                <input id="section-name" v-model="form.name" type="text" required class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Create Section</button>
        </form>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

import { useRouter } from 'vue-router';

const form = ref({
    name: ''
});

const rout = useRouter();

const createSection = async () => {
    try{
        const response = await axios.post('section', form.value);
        console.log(response.data);
        alert("Section created successfully!");
        rout.push('/');
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
</script>