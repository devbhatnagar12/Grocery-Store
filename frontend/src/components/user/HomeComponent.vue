<template>
    <div class="container">
      <div class="filters">
        <div class="filter-item">

          <input v-model="filterSection" id="filterSection" class="form-control" placeholder="Enter section name">
        </div>
        <div class="filter-item">
         
          <input v-model="filterMinPrice" type="number" id="filterMinPrice" class="form-control" placeholder="Enter min price">
        </div>
        <div class="filter-item">

          <input v-model="filterMaxPrice" type="number" id="filterMaxPrice" class="form-control" placeholder="Enter max price">
        </div>
      </div>
  
      <div v-for="section in filteredSections" :key="section.id">
        <h2 v-if="section.products.length > 0" >{{ section.name }}</h2>
        <div class="row row-cols-1 row-cols-md-3">
          <div v-for="product in filteredProducts(section.products)" :key="product.id" class="col mb-3">
            <div class="card">
              <div class="m-3">
                <h3 class="card-title mb-0 abc">{{ product.name }}</h3>
              </div>
              <div class="card-body">
                <p class="card-text">{{ product.description }}</p>
                <p class="card-text"><strong>Price: Rs. {{ product.price }}/{{ product.unit }}</strong></p>
                <template v-if="isInCart(product.id)">
                  <button @click="router.push('/cart')" class="btn btn-success">In Cart</button>
                </template>
                <template v-else>
                <select v-model="product.quantity" class="form-select">
                  <option disabled value="">Select quantity</option>
                  <option v-for="n in product.stock" :key="n" :value="n">{{ n }}</option>
                </select>
                <p v-if="product.stock === 0" class="text-danger">Out of Stock</p>
                <button @click="addToCart(product)" :disabled="isAddToCartDisabled(product)" class="btn btn-warning mt-3">Add to Cart</button>
              </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .card {
    width: 100%;
  }
  .abc{
    background-color: #fff;
  }
  
  .filters {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .filter-item {
    flex: 0 0 30%;
  }
  
  .form-control {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .label {
    margin-bottom: 5px;
  }
  </style>
  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted, computed } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  
  const sections = ref([]);
  const cart = ref([]);
  const filterSection = ref('');
  const filterMinPrice = ref(null);
  const filterMaxPrice = ref(null);
  
  const filteredSections = computed(() => {
    return sections.value.filter(section => {
      const sectionName = section.name.toLowerCase();
      return sectionName.includes(filterSection.value.toLowerCase());
    });
  });
  
  const filteredProducts = (products) => {
    const minPrice = filterMinPrice.value;
    const maxPrice = filterMaxPrice.value;
    return products.filter(product => {
      const productPrice = product.price;
  
      return (minPrice === null || !minPrice || productPrice >= minPrice) &&
             (maxPrice === null || !maxPrice || productPrice <= maxPrice);
    });
  };
  
  const getData = async () => {
    const response = await axios.get('section');
    sections.value = response.data;
  };
  
  const addToCart = async (product) => {
    try{
      const response = await axios.post('cart', { product_id: product.id, quantity: product.quantity });
    console.log("qqqq", response);
    if (response.data.success) {
      cart.value.push(product.id);
      await getData(); // Refresh the data
    }
    alert("Product added to cart successfully!");
    }catch(error){
      console.log("error", error);
      alert("Product not added to cart!");
    }
    getData();
    getCart();
  };
  
  const getCart = async () => {
    const response = await axios.get('cart');
    cart.value = response.data.map(item => item.product.id);
  };
  
  const isInCart = (product_id) => {
    return cart.value.includes(product_id);
  };
  
  const isAddToCartDisabled = (product) => {
    return !product.quantity || isInCart(product.id);
  };
  
  onMounted(() => {
    getData();
    getCart();
  });
  </script>
  