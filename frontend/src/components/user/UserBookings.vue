<template>
  <div class="booking-page container mt-5">
    <h1 class="mb-4">Grocery Delivery Booking</h1>
    <form @submit.prevent="submitBooking">
      <div class="form-group">
        <label for="customerName">Customer Name:</label>
        <input type="text" id="customerName" v-model="bookingData.customerName" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="bookingData.email" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" v-model="bookingData.quantity" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="pricePerItem">Price Per Item:</label>
        <input type="number" id="pricePerItem" v-model="bookingData.pricePerItem" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="totalCost">Total Cost:</label>
        <input type="text" id="totalCost" v-model="totalCost" class="form-control" readonly>
      </div>

      <button type="submit" class="btn btn-primary">Buy Now</button>
    </form>

    <div v-if="isBookingSubmitted" class="success-message mt-3 alert alert-success">
      Booking successful! Your groceries will be delivered soon.
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookingData: {
        customerName: '',
        email: '',
        deliveryDate: '',
        deliveryTime: '',
        groceryItems: '',
        quantity: 1,
        pricePerItem: 0,
      },
      totalCost: 0,
      isBookingSubmitted: false,
    };
  },
  watch: {
    'bookingData.quantity': 'calculateTotalCost',
    'bookingData.pricePerItem': 'calculateTotalCost',
  },
  methods: {
    submitBooking() {
      // You can perform actions like sending the booking data to a server here.
      // For simplicity, we'll just set a flag to indicate successful submission.
      this.isBookingSubmitted = true;
    },
    calculateTotalCost() {
      this.totalCost = this.bookingData.quantity * this.bookingData.pricePerItem;
    },
  },
};
</script>

<style scoped>
</style>
