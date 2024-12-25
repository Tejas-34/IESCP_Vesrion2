<script setup>
import { RouterView } from 'vue-router';
</script>


<template>
    <!-- Sidebar -->
    <div class="body">
        <div class="sidebar ">
            <h2 class="text-white text-center">Sponsor</h2>
            <router-link to="/Sponsor">Home</router-link>
            <router-link to="/Sponsor/UpdatePro">Update Profile</router-link>
            <router-link to="/Sponsor/CreatCamp">Create Campaign</router-link>
            <router-link to="/Sponsor/Camp">My Campaigns</router-link>
            <router-link to="/Sponsor/SearchInf">Search Influencer</router-link>
            <router-link to="/Sponsor/CampReq">Received Request</router-link>
            <router-link to="/Sponsor/CampReqTotal">Track Request</router-link>

            <button @click="logout"  class="logout-btn">Logout</button>
        </div>

        <RouterView />

    </div>


</template>


<script>
import router from "@/router";

export default {
    methods: {
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
    background-color: #2c3e50;
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
    background-color: #34495e;
    border-radius: 5px;
}

.content {
    margin-left: 350px;
    padding: 20px;
    max-width: 900px;
    margin-top: 20px;
    overflow-y: auto;
}




.card {
    margin-top: 20px;
}
</style>