<template>
    <div class="container">
        <form @submit.prevent="editSection" class="mt-5">
            <div class="mb-3">
                <label for="section-name" class="form-label">Section Name:</label>
                <input id="section-name" v-model="form.name" type="text" required class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Edit Section</button>
        </form>
    </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute ,useRouter} from 'vue-router';

const route = useRoute();

const rout = useRouter();
const sectionId = route.params.id;

const form = ref({});

const editSection = async () => {
    try {
        console.log('Editing section:', form.value, sectionId);
        const response = await axios.put(`section/${sectionId}`, { name: form.value.name });
        console.log(response.data);

    } catch (error) {
        console.error('Error editing section:', error);
        alert("Section edited successfully!");
        rout.push('/');

    }
}

const getSection = async () => {
    try {
        const response = await axios.get(`section?section_id=${sectionId}`);
        console.log("get section", response.data);
        form.value = response.data[0];
    } catch (error) {
        console.error('Error fetching section:', error);
    }
}

onMounted(() => {
    getSection();
});
</script>
