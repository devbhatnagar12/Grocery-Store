<template>
    <div class="container">
      <h1 class="my-4 text-center">Welcome to the Manager Dashboard!</h1>

      <div class="mb-4 text-center">
        <button @click ="exportProducts" class="btn btn-primary">Export CSV</button>
      </div>
  
      <div class="mb-4 text-center">
        <router-link to="/product/create" class="btn btn-success">Create Products</router-link>
      </div>
  
      <div v-for="(products, sectionName) in groupedProducts" :key="sectionName" class="mb-4">
        <h2 class="text-center">{{ sectionName }}</h2>
  
        <div class="row">
          <div v-for="product in products" :key="product.id" class="col-md-4 mb-3">
            <div class="card p-0">
              <h3 class="card-title m-3 abc">{{ product.name }}</h3>
              <div class="card-body">
                <p class="card-text">{{ product.description }}</p>
                <p class="card-text"><strong>Price: {{ product.price }}</strong></p>
  
                <div class="section-options">
                  <button @click="editProduct(product.id)" class="btn btn-warning edit-button">Edit</button>
                  <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

  
  
  

  
<script setup>
import { RouterLink, useRouter } from 'vue-router';
import axios from 'axios';
import { ref, onMounted , computed} from 'vue';
const products = ref([]);
const groupedProducts = computed(() => {
    return products.value.reduce((groups, product) => {
        const sectionName = product.section.name;
        if (!groups[sectionName]) {
            groups[sectionName] = [];
        }
        groups[sectionName].push(product);
        return groups;
    }, {});
});
const route = useRouter();
onMounted(async () => {
    // Fetch products from the API
    try {
        const response = await axios.get("/product", { params: { seller_only: true } });
        console.log("products", response.data);
        products.value = response.data;
    } catch (error) {
        console.error('Error fetching products:', error);
    }
});
const editProduct = (productID) => {
    route.push(`/product/${productID}/edit`);
    console.log(`Editing product with ID ${productID}`);
};
const deleteProduct = async (productID) => {
  try {
    // Make an API call to delete the product
    const response = await axios.delete(`/product/${productID}`);
    console.log('Product deleted:', response.data);
    // Remove the deleted product from the local data
    products.value = products.value.filter((product) => product.id !== productID);
  } catch (error) {
    console.error('Error deleting product:', error);
  }
};

// const exportProducts = async () => {
//   try {
//     const res = await axios.get('load-csv');
//     const data = res;

//     if (res.ok) {
//       const taskId = data['task-id'];
//       const intv = setInterval(async () => {
//         const csv_res = await axios.get(`products-csv/${taskId}`);

//         if (csv_res.ok) {
//           clearInterval(intv);
//           window.location.href = `/products-csv/${taskId}`;
//         }
//       }, 1000);
//     }
//   } catch (error) {
//     console.error('Error exporting products:', error);
//   }
// };

const exportProducts = async () => {
  const res = await axios.get('load-csv');
  const data = res.data; // Use res.data to access response data
  if (res.status === 200) { // Check for a successful response status
    const taskId = data['task-id'];
    
    // Create a link to the download URL
    const downloadLink = document.createElement('a');
    downloadLink.href = `/api/products-csv/${taskId}`;
    // downloadLink.href = 'backend/test.csv'
    // Specify the desired file name in the Content-Disposition header
    // downloadLink.setAttribute('download', 'test.csv');
    downloadLink.download = 'test.csv';
    // Simulate a click on the link to initiate the download
    downloadLink.click();
  }
};






</script>
  
<style scoped>
.abc{
    background-color: #fff;
}
.card{
    border: 1px solid #ccc;
    padding: 16px;
    background-color: #fff;
}

.edit-button {
  margin-right: 10px; /* Adjust the margin as needed */
}

.section-options {
    margin-top: 10px;
}
</style>