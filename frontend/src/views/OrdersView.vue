<template>
  <div class="container mt-5">
    <div class="card mb-4" v-for="(group, orderId) in groupedPurchases" :key="orderId">
      <div class="card-header">
        Order ID: {{ orderId }}
      </div>
      <div class="card-body">
        <div v-for="(purchase, index) in group" :key="purchase.id">
          <h3 class="card-title">Product: {{ purchase.product.name }}</h3>
          <p class="card-text">Quantity: {{ purchase.quantity }}</p>
          <p class="card-text">Price: Rs. {{ purchase.product.price }}</p>
          <p class="card-text">Purchase Date: {{ formatDate(purchase.purchase_date) }}</p>
       
          <hr v-if="index < group.length - 1">
        </div>
      </div>

      <div>
        <strong> &nbsp;  Order Grand Total: Rs. {{ calculateOrderGrandTotal(group) }}</strong> 
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';

const purchases = ref([]);

const groupedPurchases = computed(() => {
  return purchases.value.reduce((acc, purchase) => {
    (acc[purchase.order_id] = acc[purchase.order_id] || []).push(purchase);
    return acc;
  }, {});
});

const getPurchases = async () => {
  const response = await axios.get('purchase');
  purchases.value = response.data;
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}


const calculateOrderGrandTotal = (orderGroup) => {
  return orderGroup.reduce((total, purchase) => {
    return total + (purchase.product.price * purchase.quantity);
  }, 0);
}

onMounted(() => {
  getPurchases();
});

</script>

<style scoped>
.order-container {
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.order-header {
  font-size: 18px;
  margin-bottom: 10px;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
}

.quantity, .price, .purchase-date {
  font-size: 14px;
  margin-top: 5px;
}
</style>
