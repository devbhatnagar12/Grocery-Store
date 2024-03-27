<template>
    <div class="container">
        <h2 class="my-4">Pending requests will appear here</h2>
        <div v-for="request in requests" :key="request.id" class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">{{ request.description }}</h5>
                <p class="card-text">Requested by: {{ request.requesterEmail }}</p>
                <p class="card-text" v-if="request.sectionName">Section: {{ request.sectionName }}</p>
                <button @click="respondToRequest(request.id, 'approve')" class="btn btn-success def">Approve</button>
                <button @click="respondToRequest(request.id, 'reject')" class="btn btn-danger">Deny</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

let requests = ref([]);
console.log(requests.value)

const getRequests = async () => {
    try {
        const response = await axios.get('approvals', { params: { status: 'pending' } });
        const data = response.data;

        const updatedRequests = await Promise.all(data.map(async request => {
            try {
                const userResponse = await axios.get('user', { params: { id: request.requester_id } });
                request.requesterEmail = userResponse.data[0].email;
                if (request.section_id) {
                    console.log("section_id", request.section_id)
                    const sectionResponse = await axios.get('section', { params: { section_id: request.section_id } });
                    console.log("sectionResponse", sectionResponse)
                    request.sectionName = sectionResponse.data[0].name;
                }
            } catch (error) {
                console.error('Error fetching user or section data:', error);
            }
            console.log(request)
            return request;
        }));

        requests.value = updatedRequests;
    } catch (error) {
        console.error('Error fetching approvals:', error);
    }
}

const respondToRequest = async (id, type) => {
    console.log(type)
    const response = await axios.put(`approve/${id}?type=${type}`);
    console.log(response.data);
    getRequests(); // Refresh the requests after responding
}

onMounted(() => {
    getRequests();
});
</script>

<style scoped>
    .def {
        margin-right: 10px;
    }
</style>