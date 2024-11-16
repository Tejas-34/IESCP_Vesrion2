<template>
    <div class="col-md-9 col-lg-10 content">
        <!-- Header Section -->
        <div class="header-section bg-primary text-white p-4 rounded mb-4">
            <h1 class="text-center mb-0">Influencer Requests</h1>
            <p class="text-center">Manage requests from influencers for your campaigns.</p>
        </div>

        <!-- Request Cards -->
        <div class="row">
            <div class="col-lg-6 mb-4" v-for="(request, index) in allData" :key="index">
                <div class="card shadow-sm h-100">
                    <!-- Influencer Information -->
                    <div class="card-header bg-info text-white">
                        <h5 class="card-title mb-0">
                             {{ request.InfName }}
                        </h5>
                        <small class="text-white">Reach: {{ request.InfReach }} followers</small>
                    </div>

                    <!-- Campaign Details -->
                    <div class="card-body">
                        <p><strong>Campaign:</strong> {{ request.CampName }}</p>
                        <p><strong>Message:</strong> {{ request.message[0].message }}</p>
                        <p><strong>Demanded Amount:</strong> {{ request.payment_amount }}</p>
                    </div>

                    <!-- Action Buttons -->
                    <div class="card-footer d-flex justify-content-between align-items-center">
                    <button class="btn btn-success btn-sm me-2" @click="handleAction('Accepted', request.id)"
                        v-if="request.status === 'Pending'">
                        Approve
                    </button>
                    <button class="btn btn-danger btn-sm me-2" @click="handleAction('Rejected', request.id)"
                        v-if="request.status === 'Pending'">
                        Reject
                    </button>
                    <button class="btn btn-warning btn-sm me-2" @click="handleAction('Negotiating', request.id)"
                        v-if="request.status === 'Pending'">
                        Negotiate
                    </button>
                    <button class="btn btn-info btn-sm me-2" @click="Negotiate(request.id)"
                        v-if="request.status === 'Negotiating'">
                         Continue Negotiation
                    </button>
                    <span v-if="request.status != 'Pending'"
                                class="badge"
                                :class="{
                                    'bg-success': request.status === 'Accepted',
                                    'bg-danger': request.status === 'Rejected',
                                    'bg-warning': request.status === 'Pending',
                                }"
                                >
                                {{ request.status }}
                    </span>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>

import router from "@/router";

export default {
    data() {
        return {
            
            allData:[],
        };
    },

    created() {
        this.fetchReqestData();
    },

    methods: {

        fetchReqestData() {
            // Fetch data from backen
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/requests',
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
                        this.allData = data.combine.slice().reverse();
                        this.campaign = data.campaign.slice().reverse();
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },


        handleAction(action, id) {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/request/update/' + id, {
                method: 'PUT',
                headers: {
                    'Authorization': 'Bearer ' + local.token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'status': action })
            }).then(response => {
                if (response.status == 401) {
                    router.push('/login')
                }
                else if (!response.status == 200) {
                    alert('Something went wrong...');
                }
                else {
                    alert('request has been ' + action)
                    this.fetchReqestData();

                }
            })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        Negotiate(id) {
            router.push({ name: 'SpoNegotiation', params: { id: id } });
        },
    },


};
</script>







<style scoped>
.header-section {
    text-align: center;
    border-radius:10px;
    margin-bottom: 20px;
    background: linear-gradient(90deg, #4caf50, #2196f3);
    color: white;
}

.card {
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.card-header {
    font-weight: bold;
    font-size: 1.1rem;
}

.card-footer .btn {
    width: 30%;
}

.card-footer .btn i {
    margin-right: 5px;
}
</style>


