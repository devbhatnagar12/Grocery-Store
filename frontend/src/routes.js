import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { name: 'Home', path: '/', component: () => import('./views/HomeView.vue') },
    { name: 'Login', path: '/login', component: () => import('./views/LoginView.vue') },
    { name: 'Register', path: '/register', component: () => import('./views/RegisterView.vue') },
    { name: 'CreateSection', path: '/section/create', component: () => import('./views/CreateSectionView.vue'), meta: { roles: ['manager', 'admin'] } },
    {name: 'EditSection', path: '/section/:id/edit', component: () => import('./views/EditSection.vue'), meta: { roles: ['admin', 'manager'] } },
    {name: 'EditProduct', path: '/product/:id/edit', component: () => import('./views/EditProduct.vue'), meta: { roles: ['manager'] } },
    { name: 'CreateCategory', path: '/createcategory', component: () => import('./components/manager/CreateCategory.vue'), meta: { roles: ['manager', 'admin'] } },
    { name: 'NewProduct', path: '/product/create', component: () => import('./views/NewProductView.vue'), meta: { roles: ['manager'] } },
    { name: "Cart", path: '/cart', component: () => import('./views/CartView.vue') },
    { name: "Orders", path: '/orders', component: () => import('./views/OrdersView.vue'), meta: { roles: ['user'] }},
    { name: "Order", path: '/order/:id', component: () => import('./views/OrderView.vue'), meta: { roles: ['user'] }},
    { name: 'UserProfile', path: '/userprofile', component: () => import('./components/user/UserProfile.vue'), meta: { roles: ['user'] } },
    { name: 'UserBookings', path: '/userbookings', component: () => import('./components/user/UserBookings.vue'), meta: { roles: ['user'] } },
    { name: 'UserDashboard', path: '/userdashboard', component: () => import('./components/user/UserDashboard.vue'), meta: { roles: ['user'] } },
    { name: 'Unauthorized', path: '/unauthorized', component: () => import('./views/UnauthorizedView.vue') },
    {name: 'AdminRequests', path: '/adminrequests', component: () => import('./components/admin/AdminRequests.vue'), meta: { roles: ['admin'] }},
    {name: 'RequestSection', path: '/newrequest', component: () => import('./views/RequestSection.vue'), meta: { roles: ['manager'] }},
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

import axios from 'axios';


router.beforeEach(async (to, from, next) => {
    const publicPages = ['/login', '/register'];
    const authRequired = !publicPages.includes(to.path);
    const token = localStorage.getItem('token');

    if (token) {
        try {
            const email = localStorage.getItem('email');
            const role = localStorage.getItem('role');
            const response = await axios.post('/auth/verify', { email, role });

            if (response.status === 200) {
                if (to.meta.roles && !to.meta.roles.includes(role)) {
                    return next('/unauthorized');
                }

                if (publicPages.includes(to.path)) {
                    return next('/');
                }

                next();
            } else {
                if (authRequired) {
                    next('/login');
                } else {
                    next();
                }
            }
        } catch (error) {
            console.error(error);
            if (authRequired) {
                next('/login');
            } else {
                next();
            }
        }
    } else if (authRequired && !token) {
        next('/login');
    } else {
        next();
    }
});

export default router;