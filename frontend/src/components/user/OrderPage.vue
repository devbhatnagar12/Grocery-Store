<template>
    <div class="container mt-5">
      <h2 class="mb-4">Order History</h2>
  
      <ul class="list-group">
        <li v-for="order in orders" :key="order.id" class="list-group-item">
          <h3 class="mb-3">Order ID: {{ order.id }}</h3>
          <p class="mb-2"><strong>Order Date:</strong> {{ order.date }}</p>
          <ul class="list-group">
            <li v-for="item in order.items" :key="item.id" class="list-group-item">
              {{ item.name }} - Quantity: {{ item.quantity }} - Price: ${{ item.price.toFixed(2) }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  const orders = [
    {
      id: 1,
      date: '2024-01-20',
      items: [
        { id: 101, name: 'Item A', quantity: 2, price: 5.99 },
        { id: 102, name: 'Item B', quantity: 1, price: 7.49 }
      ]
    },
    {
      id: 2,
      date: '2024-01-19',
      items: [
        { id: 201, name: 'Item C', quantity: 3, price: 3.99 },
        { id: 202, name: 'Item D', quantity: 2, price: 9.99 }
      ]
    },
    {
      id: 3,
      date: '2024-01-19',
      items: [
        { id: 201, name: 'Item C', quantity: 3, price: 3.99 },
        { id: 202, name: 'Item D', quantity: 2, price: 9.99 }
      ]
    },
    {
      id: 4,
      date: '2024-01-19',
      items: [
        { id: 201, name: 'Item C', quantity: 3, price: 3.99 },
        { id: 202, name: 'Item D', quantity: 2, price: 9.99 }
      ]
    },
    {
      id: 5,
      date: '2024-01-19',
      items: [
        { id: 201, name: 'Item C', quantity: 3, price: 3.99 },
        { id: 202, name: 'Item D', quantity: 2, price: 9.99 }
      ]
    },

  ];
  </script>
  
  <style scoped>
  </style>
  