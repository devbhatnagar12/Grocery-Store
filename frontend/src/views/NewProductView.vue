<template>
  <div class="container mt-5">
    <h2 class="mb-4">Create a New Product</h2>
    <form @submit.prevent="saveProduct">
      <div class="mb-3">
        <label for="productName" class="form-label">Product Name:</label>
        <input
          type="text"
          id="productName"
          class="form-control"
          v-model="product.name"
          required
        />
      </div>

      <div class="mb-3">
        <label for="productDescription" class="form-label"
          >Product Description:</label
        >
        <textarea
          id="productDescription"
          class="form-control"
          v-model="product.description"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="productSection" class="form-label">Section:</label>
        <select
          id="productSection"
          class="form-select"
          v-model="product.section_id"
          required
        >
          <option
            v-for="section in sections"
            :key="section.id"
            :value="section.id"
          >
            {{ section.name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label for="productUnit" class="form-label">Unit:</label>
        <select
          id="productUnit"
          class="form-select"
          v-model="product.unit"
          required
        >
          <option value="Kg">₹/Kg</option>
          <option value="L">₹/Litre</option>
          <option value="dozen">₹/dozen</option>
          <option value="g">₹/grams</option>
          <option value="N">₹/N</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="productRate" class="form-label">Price:</label>
        <input
          type="number"
          id="productRate"
          class="form-control"
          v-model="product.price"
          required
        />
      </div>

      <div class="mb-3">
        <label for="productStock" class="form-label">Stock:</label>
        <input
          type="number"
          id="productStock"
          class="form-control"
          v-model="product.stock"
          required
        />
      </div>

      <div class="mb-3">
        <label for="productExpirationDate" class="form-label"
          >Expiration Date:</label
        >
        <input
          type="date"
          id="productExpirationDate"
          class="form-control"
          v-model="product.expired_at"
          required
        />
      </div>

      <div>
        <button type="submit" class="btn btn-primary">Save</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const product = ref({
  name: "",
  description: "",
  unit: "₹/Kg", // Default unit
  price: 0,
  stock: 0,
  section_id: 0,
  expired_at: "",
});

const sections = ref([]);
const router = useRouter();

const saveProduct = async () => {
  try{
    const response = await axios.post('product', product.value);
    console.log(response.data);
    // alert("Product created successfully!");
    router.push('/');
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const getSections = async () => {
  try{
    const response = await axios.get("section", { params: { active: true } });
  console.log(response.data);
  // Check if response.data is an array before calling map
  if (Array.isArray(response.data)) {
    sections.value = response.data.map((section) => {
      return {
        id: section.id,
        name: section.name,
      };
    });
  } else {
    sections.value = [{ id: response.data.id, name: response.data.name }];
    console.log(sections.value);
  }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
 
};

onMounted(() => {
  getSections();
});
</script>
