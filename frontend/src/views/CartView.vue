<template>
    <div class="container">
      <h1>Cart</h1>
      <div class="row">
        <div class="col-12">
          <table class="table">
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Price</th>
                <th>Unit</th>
                <th>Quantity</th>
                <th>Total</th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in cart" :key="item.id">
                <td>{{ item.product.name }}</td>
                <td>{{ item.product.price }}</td>
                <td>{{ item.product.unit }}</td>
                <td>
                  <input type="number" v-model="item.quantity" @input="checkQuantity(item)" min="1">
                </td>
                <td>{{ itemTotal(item) }}</td>
                <td>
                  <button class="btn btn-primary" @click="updateQuantity(item)">Update</button>
                </td>
                <td>
                  <button class="btn btn-danger" @click="deleteItem(item.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="text-right">
          <strong v-if="grandTotal > 0">Grand Total: Rs. {{ grandTotal }}</strong>
        </div>
        <button class="btn btn-success mt-3" @click="purchase" v-if="grandTotal > 0">Buy Now</button>

        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted, computed } from 'vue';
  import { useRouter } from 'vue-router';
  
  const cart = ref([]);
  const router = useRouter();
  
  const getCart = async () => {
      try {
          const response = await axios.get('/cart');
          cart.value = response.data;
          console.log("cart value", cart.value)
      } catch (error) {
          console.error('Error fetching data:', error);
      }
  }
  
  const itemTotal = (item) => {
      return item.product.price * item.quantity;
  }
  
  const grandTotal = computed(() => {
      return cart.value.reduce((total, item) => {
          return total + itemTotal(item);
      }, 0);
  });
  
  const purchase = async () => {
      try {
          const response = await axios.post('/purchase');
          console.log(response.data);
          alert("Order placed successfully!");
          router.push('/order/' + response.data.order_id);
      } catch (error) {
          console.error('Error fetching data:', error);
      }
  }
  
  const deleteItem = async (itemId) => {
      try {
          await axios.delete(`/cart/${itemId}`);
          cart.value = cart.value.filter(item => item.id !== itemId);
      } catch (error) {
          console.error('Error deleting item:', error);
      }
  }
  
  const updateQuantity = async (item) => {
      try {
          await axios.put(`/cart/${item.id}`, {product_id: item.product.id, quantity: item.quantity });
          getCart();
      } catch (error) {
          console.error('Error updating quantity:', error);
      }
  }
  
  const checkQuantity = (item) => {
      if (item.quantity > item.product.stock) {
          item.quantity = item.product.stock;
      }
  }
  
  onMounted(() => {
      getCart();
  });
  </script>
  