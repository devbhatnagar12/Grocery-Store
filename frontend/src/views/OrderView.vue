<template>
    <div class="container">
        <h1>Order Details</h1   >
        <div class="row">
            <div class="col-12">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in orderDetails" :key="item.id">
                            <td>{{ item.product.name }}</td>
                            <td>{{ item.product.price }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>{{ item.product.price * item.quantity }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();


const orderId = route.params.id;
console.log(orderId);
const orderDetails = ref([]);

const getOrderDetails = async () => {
    try{
        const response = await axios.get(`purchase`, { params: { order_id: orderId }});
        orderDetails.value = response.data;
        console.log(response.data);
    } catch (error) {
        console.error('Error fetching data:', error);
    
    }
}

onMounted(() => {
    getOrderDetails();
});

</script>