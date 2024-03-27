<template>

    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 mt-5 form">
                <form @submit.prevent="register" class="border rounded p-3 shadow">
                    <h2 class="text-center mb-4">Create an account</h2>
                    <div class="mb-3">
                        <label for="role" class="form-label">Role</label>
                        <select v-model="form.role" class="form-control" id="role" required>
                            <option>user</option>
                            <option>manager</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email address</label>
                        <input v-model="form.email" type="email" class="form-control" id="email"
                            aria-describedby="emailHelp" required>
                        <div id="emailHelp" class="form-text warn">We'll never share your email with anyone else.</div>
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input v-model="form.password" type="password" class="form-control" id="password" required>
                    </div>

                    <div class="mb-3">
                        <label for="confirmPassword" class="form-label">Confirm Password</label>
                        <input v-model="form.confirmPassword" type="password" class="form-control" id="confirmPassword"
                            required>
                        <div v-if="!passwordsMatch" class="text-danger abc">Passwords do not match</div>
                    </div>

                    <div class="d-grid gap-2">
                        <button :disabled="!isFormValid" type="submit" class="btn btn-primary">Create Account</button>
                    </div>

                    <div class="text-center mt-3">
                        <span class="warn">Already have an account?  </span>
                        <router-link class="warn" to="/login">Log in</router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = ref({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'user',
    passwordsMatch: true,
});

const passwordsMatch = computed(() => {
    return form.value.password === form.value.confirmPassword;
});

const isFormValid = computed(() => {
    return form.value.email && form.value.password && form.value.confirmPassword && passwordsMatch.value;
});

const register = async () => {
   
    if (!passwordsMatch.value) {
        console.log('passwords do not match')
        return;
    }
    else {
        console.log('passwords match')
        console.log(form.value)
    }

    await axios.post('user', form.value)
        .then(() => {
            
            console.log('User registered successfully!');
            router.push('/');
        })
        .catch((error) => {
          
            console.error('Error registering:', error.response.data);
        });
};
</script>
  
<style scoped>
form {
    background-color: #fff;
    padding: 20px;
}
.form{
    margin: 0;
    padding: 0;
    border: 3px solid #000000;
}
.warn{
    background-color: #fff;
}
form {
  background-color: #fff;
  padding: 20px;
}
h1, h2, h3, h4, h5, h6, label, input, button {
    background-color: #fff;
}
form > div {
    background-color: #fff;
}
.regnew{
    background-color: #fff;
}

.btn-primary {
    background-color: #000000;
    border-color: #141516;
}

.btn-primary:hover {
    background-color: #183654;
    border-color: rgb(30, 41, 53);
}

.btn-primary:focus {
    box-shadow: 0 0 0 0.25rem rgba(38, 143, 255, 0.5);
}

.text-danger {
    font-size: 0.875rem;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.abc{
    background-color: #fff;
}
</style>
  