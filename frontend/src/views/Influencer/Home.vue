<template>
    <div class="col-md-9 col-lg-10 content">
        <div class="welcome-section text-dark p-2 rounded mb-3">
            <h1 class="mb-0" align="center"> Welcome to Your Dashboard!</h1>
        </div>

        <!-- Overview Boxes -->
        <div class="row mb-4">
            <!-- Total Earnings Box -->
            <div class="col-md-6">
                <div class="card stats-card shadow p-3 mb-5 bg-body rounded earnings-box">
                    <div class="card-body text-center"> 
                        <h5>Total Earnings</h5>
                        <p class="display-6 text-success">${{ earning }}</p>
                    </div>
                </div>
            </div>

            <!-- Total Pending Requests Box -->
            <div class="col-md-6">
                <div class="card stats-card shadow p-3 mb-5 bg-body rounded pending-box">
                    <div class="card-body text-center">
                        <h5>Total Pending Requests</h5>
                        <p class="display-6 text-warning">{{ pending }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- User Info Section -->
        <div class="card shadow-sm mb-4">
            <div class="card-header bg-info text-white">
                <h5 class="card-title mb-0">Your Profile</h5>
            </div>
            <div class="card-body">
                <div class="user-info row">
                    <div class="col-md-6">
                        <p> <strong>Name:</strong> {{ influencer.name }}</p>
                        <p><strong>Email:</strong> {{ influencer.email }}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Reach:</strong> {{ influencer.Reach }} followers</p>
                        <p> <strong>Category:</strong> {{ influencer.Category }}</p>
                    </div>
                    <div class="col-md-12">
                        <p> <strong>Niche:</strong> {{ influencer.Niche }}</p>
                        <p><strong>Bio:</strong> {{ influencer.bio }}</p>
                    </div>
                </div>
            </div>
        </div>


        <!-- Accepted Campaigns Section -->
        <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
                <h5 class="card-title mb-0">Accepted Campaigns</h5>
            </div>
            <div class="card-body">
                <div class="list-group" v-for="(request, index) in requests" :key="request.id" >
                    <button  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0">Campaign {{ index+1 }} - {{ request.CampName }}</h6>
                            <p class="mb-0 small">Duration: {{ request.duration }} days | Payment: ${{ request.payment_amount }}</p>
                        </div>
                        <span class="badge bg-primary rounded-pill">${{ request.payment_amount }}</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>



<script>

import router from '@/router';

export default {
    data() {
        return {
            influencer: [],
            requests: [],
            earning: 0,
            pending: 0,
        };
    },
    
    created() {
        this.fetchInfluencerData();
        this.fetchAccptedReqData();
    },
    
    methods: {
        fetchInfluencerData() {
            const local = JSON.parse(localStorage.getItem("user"));
            
            console.log(local.token)
            fetch(import.meta.env.VITE_BASEURL + '/influencer/' + local.user_id,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + local.token, // Include token in header
                        'Content-Type': 'application/json',
                    },
                    
                }).then(response => {
                    if (response.status == 401) {
                        router.push('/login')
                    }
                    return response.json();
                })
                .then(data => {
                    if (data) {
                        console.log(data);
                        this.influencer = data;
                    }
                })
                .catch(error => console.error("Error fetching influencer data:", error));
        },
        
        
        fetchAccptedReqData(){
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/accepted',
                {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + local.token,
                        'Content-Type': 'application/json',
                    },
                    
                }).then(response => {
                    if (response.status == 401) {
                        router.push('/login')
                    }
                    else if (!response.status == 200) {
                        alert('Something went wrong...');
                    }
                    return response.json() || {};
                })
                .then(data => {
                    if (data) {
                        console.log(data);
                        this.requests = data.data.slice().reverse();
                        this.earning = data.earning;
                        this.pending = data.pending;
                        
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        }
    }



}
</script>



    <style scoped>
    
    
    .card {
        margin-top: 20px;
        border-radius: 10px;
    }
    
    .card-header {
        font-weight: bold;
    }
    
    .user-info p {
        margin-bottom: 10px;
        font-size: 1rem;
    }
    
    .display-6 {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .list-group-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .list-group-item h6 {
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    .list-group-item .badge {
        font-size: 0.9rem;
        padding: 0.5em 1em;
    }
    
    .list-group-item p {
        font-size: 0.85rem;
        color: #6c757d;
    }

    .stats-card {
    background-color: #ffffff;
    border-radius: 10px;
    transition: transform 0.2s;
}



.stats-card:hover {
    transform: scale(1.05);
}



    </style>

