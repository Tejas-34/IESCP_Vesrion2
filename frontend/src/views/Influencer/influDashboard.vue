<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <div class="container-fluid" style="background-color: aliceblue;">
        <div class="row">

            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar">
                <h2 class="text-white">Influencer</h2>
                <router-link to="/influencer">Home</router-link>
                <router-link to="/influencer/infupdate">Update Profile</router-link>
                <router-link to="/influencer/AdRequest">Ad Request</router-link>
                <router-link to="/influencer/s_camp">Search Campaign</router-link>
                <router-link to="/AllRequest">Track Request</router-link>
                <button class="logout-btn" @click="logout">Logout</button>
                
            </div>

            <!-- Main Content -->
            <RouterView />
        </div>
    </div>
</template>

<script>

import router from "@/router";

export default {
    data() {
        return {
            username: null,
            password: null,
            log: false
        }
    },
    methods:{
        logout(){
            localStorage.removeItem('token');
            localStorage.removeItem("user");
            router.push('/login');
        }
    }
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

.sidebar button.logout-btn {
    background-color: transparent;
    border: none;
    color: #ffffff;
    text-decoration: none;
    padding: 10px 20px;
}

.sidebar button.logout-btn:hover {
    background-color: #495057;
    border-radius: 5px;
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