<template>
  <div>
    <ManagerNavbar/>
      <h2>Add a Category</h2>
      <button @click="openModal" class="btn btn-primary" v-show="!isModalOpen">Add Category</button>
  
      <!-- Modal -->
      <div v-show="isModalOpen">
        <h4>Creating a new category</h4>
        <div class="mb-5">
          <label for="newCategoryName" class="text-left">Category Name:</label>
          <input type="text" id="newCategoryName" v-model="newCategoryName" required>
        </div>
        <div>
          <button @click="saveCategory" class="btn btn-primary">Save</button>
        </div>
      </div>
  
      <!-- Display Categories -->
      <div>
        <h4>Categories</h4>
        <div class="category-cards">
          <div v-for="category in categories" :key="category.id" class="category-card">
            <div class="card">
              <div class="card-body text-center">
                <h5 class="card-title">{{ category.name }}</h5>
                <div class="">
                    <router-link to="/newproduct" class="btn btn-info mt-5">+</router-link>
                </div>
                
                <div class="category-buttons mt-5">
                  <button class="btn btn-primary p-2">Edit</button>
                  <button class="btn btn-danger p-2">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>


<script>
import ManagerNavbar from "./ManagerNavbar.vue"; 
  export default {
    components: {
    ManagerNavbar
  },
    data() {
      return {
        isModalOpen: false,
        newCategoryName: "",
        categories: [], // Your category data should be loaded here
      };
    },
    methods: {
      openModal() {
        this.isModalOpen = true;
        this.newCategoryName = ""; // Clear the input field when opening the modal
        console.log("openModal", this.isModalOpen);
      },
      closeModal() {
        this.isModalOpen = false;
      },
      saveCategory() {
        const newCategory = {
          id: this.categories.length + 1, // You should generate a unique ID
          name: this.newCategoryName,
        };
        this.categories.push(newCategory);
        this.closeModal();
      },
    },
  };
  </script>
  
  <style scoped>
  .category-cards {
    display: flex;
    flex-wrap: wrap;
  }
  
  .category-card {
    margin: 10px;
  }
  
  .category-buttons button {
    margin-right: 5px;
  }
  </style>
  