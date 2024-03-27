<template>
  <div class="grocery-list container mt-5">
    <h1 class="mb-4">Grocery Items</h1>

    <div class="row">
      <div v-for="item in groceryItems" :key="item.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <img :src="getImageUrl(item.category)" class="card-img-top" alt="Grocery Item Image">
          <div class="card-body">
            <h5 class="card-title">{{ item.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ item.category }}</h6>
            <p class="card-text">Price: ${{ item.price.toFixed(2) }}</p>
            <button @click="addToCart(item)" class="btn btn-primary">Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      groceryItems: [
        { id: 1, name: 'Apples', category: 'Fruits', price: 1.99 },
        { id: 2, name: 'Milk', category: 'Dairy', price: 2.49 },
        { id: 2, name: 'Milk', category: 'Dairy', price: 2.49 },
        { id: 2, name: 'Milk', category: 'Dairy', price: 2.49 },
        { id: 2, name: 'Milk', category: 'Dairy', price: 2.49 },
      ],
    };
  },
  methods: {
    addToCart(item) {
      console.log(`Added ${item.name} to the cart!`);
    },
    getImageUrl(category) {
      return `https://placekitten.com/300/200?category=${category}`;
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
}

.card-img-top {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}
</style>
