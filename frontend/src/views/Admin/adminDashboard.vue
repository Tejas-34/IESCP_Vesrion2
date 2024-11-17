<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <div class="container-fluid" style="background-color: aliceblue;">
        <div class="row">

            <!-- Sidebar -->
            <aside class="col-md-3 col-lg-2 sidebar">
                <h2 class="text-white">Admin</h2>
                <router-link to="/admin">Home</router-link>
                <router-link to="/admin">Statistics</router-link>
                <router-link to="/admin/user">User Management</router-link>
                <router-link to="/admin">Campaigns</router-link>
                <router-link to="/admin">Flagged Content</router-link>
                <a href="/login">Logout</a>
                
            </aside>


            <!-- Main Content -->
            <RouterView />
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            username: null,
            password: null,
            log: false
        }
    },
}

</script>


<style scoped>
.sidebar {
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    background-color: #343a40;
    padding-top: 20px;
    overflow-y: auto;


}

.sidebar a {
    color: #ffffff;
    text-decoration: none;
    padding: 10px 20px;
    display: block;
    font-weight: 500;
    margin-bottom: 10px;
}

.sidebar a:hover {
    background-color: #495057;
    border-radius: 5px;
}


.content {
    margin-left: 350px;
    padding: 20px;
    max-width: 1000px;
    margin-top: 20px;
    overflow-y: auto;
}

.card {
    margin-top: 20px;
}

.container-fluid{
    min-height: 850px;
}
</style>