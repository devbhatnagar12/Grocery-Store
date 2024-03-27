<template>
    <div class="container mt-5">
      <form @submit.prevent="editProduct" class="mt-5">
        <div class="mb-3">
          <label for="productName" class="form-label">Product Name:</label>
          <input type="text" id="productName" v-model="form.name" class="form-control" required>
        </div>
  
        <div class="mb-3">
          <label for="productDescription" class="form-label">Product Description:</label>
          <textarea id="productDescription" v-model="form.description" class="form-control" required></textarea>
        </div>
  
        <div class="mb-3">
          <label for="productSection" class="form-label">Section:</label>
          <select id="productSection" v-model="form.section_id" class="form-select" required>
            <option v-for="section in sections" :key="section.id" :value="section.id">
              {{ section.name }}
            </option>
          </select>
        </div>
  
        <div class="mb-3">
          <label for="productUnit" class="form-label">Unit:</label>
          <select id="productUnit" v-model="form.unit" class="form-select" required>
            <option value="Kg">₹/Kg</option>
            <option value="L">₹/Litre</option>
            <option value="dozen">₹/dozen</option>
            <option value="g">₹/grams</option>
            <option value="N">₹/N</option>
          </select>
        </div>
  
        <div class="mb-3">
          <label for="productRate" class="form-label">Price:</label>
          <input type="number" id="productRate" v-model="form.price" class="form-control" required>
        </div>
  
        <div class="mb-3">
          <label for="productstock" class="form-label">Stock:</label>
          <input type="number" id="productstock" v-model="form.stock" class="form-control" required>
        </div>
  
        <div class="mb-3">
          <label for="productExpirationDate" class="form-label">Expiration Date:</label>
          <input type="date" id="productExpirationDate" v-model="form.expired_at" class="form-control" required>
        </div>
  
        <button type="submit" class="btn btn-primary">Edit Product</button>
      </form>
    </div>
  </template>
  

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute,useRouter } from 'vue-router';

const route = useRoute();
const productId = route.params.id;

const form = ref({});
const router = useRouter();
const sections = ref([]);

const editProduct = async () => {
    try {
        console.log('Editing section:', form.value, productId);
        const response = await axios.put(`product/${productId}`, form.value);
        console.log(response.data);
        router.push('/');
    } catch (error) {
        console.error('Error editing section:', error);
        router.push('/');
    }
}

const getProduct = async () => {
    try {
        const response = await axios.get(`product`, { params: { product_id: productId } });
        console.log(response.data);
        form.value = response.data[0];
    } catch (error) {
        console.error('Error getting product:', error);
    }
}

const getSections = async () => {
    try {
        const response = await axios.get(`section`, { params: { active: true } });
        console.log(response.data);
        sections.value = response.data;
    } catch (error) {
        console.error('Error getting sections:', error);
    }
}

onMounted(() => {
    getProduct();
    getSections();
});
</script>
