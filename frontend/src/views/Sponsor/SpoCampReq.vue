<template>
    <div class="col-md-9 col-lg-10 content">
        <!-- Header Section -->
        <div class="header-section bg-primary text-white p-4 rounded mb-4">
            <h1 class="text-center mb-0">All Received Requests</h1>
            <p class="text-center">View all requests from influencers for your campaigns.</p>
        </div>

        <!-- Requests Table -->
        <div class="table-responsive">
            <table class="table table-bordered table-hover shadow-sm">
                <thead class="table-light">
                    <tr>
                        <th>#</th>
                        <th>Influencer Name</th>
                        <th>Campaign Title</th>
                        <th>Payment</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in allData" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.InfName }}</td>
                        <td>{{ request.CampName}}</td>
                        <td>${{ request.payment_amount }}</td>
                        <td>
                            <span v-if="request.status != 'Negotiating'"
                                class="badge"
                                :class="{
                                    'bg-success': request.status === 'Accepted',
                                    'bg-danger': request.status === 'Rejected',
                                    'bg-warning': request.status === 'Pending',
                                }"
                                >
                                {{ request.status }}
                            </span>

                            <button v-else class="bg-info badge" @click="Negotiate(request.id)" style="border: none;" :style="{ display: (request.status === 'Negotiating') ? 'block' : 'none' }"> {{request.status}}</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import router from "@/router";

export default {
    data() {
        return {
            requests: [],
            campaign: [],
            allData:[],
        }
    },

    created() {
        this.fetchReqestData();
    },

    methods: {

        fetchReqestData() {
            // Fetch data from backen
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/allrequests',
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
                        this.allData = data.request.slice().reverse();
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },
        Negotiate(id) {
            router.push({ name: 'SpoNegotiation', params: { id: id } });
     },
    },
    
    
}

</script>

<style scoped>
.header-section {
    text-align: center;
    border-radius: 8px;
    margin-bottom: 20px;
    background: linear-gradient(90deg, #4caf50, #2196f3);
    color: white;
}

.table {
    margin-top: 20px;
    border-collapse: collapse;
    font-size: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.table-hover tbody tr:hover {
    background-color: #f9f9f9;
}

.badge {
    font-size: 0.9rem;
    padding: 5px 10px;
    border-radius: 10px;
}

.bg-success {
    background-color: #28a745 !important;
    color: white;
}

.bg-danger {
    background-color: #dc3545 !important;
    color: white;
}

.bg-warning {
    background-color: #ffc107 !important;
    color: black;
}

.bg-info {
    background-color: #17a2b8 !important;
    color: white;
}
</style>
