<template>
    <div class="user-profile">
        <div class="user-info">
            <h2>Dev Bhatnagar</h2>
            <p>dev@gmail.com</p>
        </div>
    </div>
</template>
  
<script setup>
</script>
  
<style scoped>
.user-profile {
    display: flex;
    align-items: center;
    margin: 20px;
}

.avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-right: 20px;
}

.user-info {
    flex-grow: 1;
}

h2 {
    margin: 0;
}

p {
    margin: 5px 0;
    color: #888;
}
</style>
  