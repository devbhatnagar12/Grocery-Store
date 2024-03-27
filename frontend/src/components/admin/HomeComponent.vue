<template>
  <div class="d-flex flex-column align-items-center vh-100">
    <div>
      <h1 class="my-4">Welcome to the Admin dashboard!</h1>
      <div class="mb-4 d-flex justify-content-center"> 
        <router-link to="/section/create" class="btn btn-success">Create Section</router-link>
      </div>
    </div>

    <div class="container">
      <div class="row row-cols-1 row-cols-md-4">
        <div v-for="section in sections" :key="section.id" class="col mb-3">
          <div class="card section-card p-0">
            <h2 class="card-title abc " >{{ section.name }}</h2>

            <div class="card-body section-options">
              <button @click="editSection(section.id)" class="btn btn-warning edit-button">Edit</button>
              <button @click="deleteSection(section.id)" class="btn btn-danger">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>







  
  <script setup>
  import { RouterLink,useRouter } from 'vue-router';
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  
  const sections = ref([]);
  const route = useRouter();
  onMounted(async () => {
    // Fetch sections from the API
    try {
      const response = await axios.get('/section?active=true');
      sections.value = response.data;
    } catch (error) {
      console.error('Error fetching sections:', error);
    }
  });
  
  const editSection = (sectionId) => {
    route.push(`/section/${sectionId}/edit`);
    console.log(`Editing section with ID ${sectionId}`);
  
};
  
  const deleteSection = async (sectionId) => {
    try {
      // Make an API call to delete the section
      alert("Are you sure you want to delete this section?")
      const response = await axios.delete(`/section/${sectionId}`);
      console.log('Section deleted:', response.data);
  
      // Remove the deleted section from the local data
      sections.value = sections.value.filter(section => section.id !== sectionId);
    } catch (error) {
      console.error('Error deleting section:', error);
    }
  };
  </script>
  
  <style scoped>
  .section-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }
  
  .abc{
    background-color: #fff;
  }
  .section-card {
    border: 1px solid #ccc;
    padding: 16px;
    text-align: center;
  }

  .edit-button {
  margin-right: 10px; 
}
  
  .section-options {
    margin-top: 5px;
  }
  </style>
  