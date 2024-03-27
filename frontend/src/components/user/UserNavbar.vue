<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand abc" to="/">User Dashboard</router-link>

    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse abc" id="navbarNav">
      <ul class="navbar-nav abc">

        <li class="nav-item abc">
          <router-link class="nav-link abc" to="/cart">Cart</router-link>
        </li>
        <li class="nav-item abc">
          <router-link class="nav-link abc" to="/orders">Previous Orders</router-link>
        </li>
        <li class="nav-item abc">
          <button class="nav-link abc" @click="logout">Log Out</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { logout } from '@/helpers/authHelper';

</script>

<style scoped>
.abc{
  background-color: #F8F9FA;
}
</style>
