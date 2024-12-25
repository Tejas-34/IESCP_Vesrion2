<template>
    <div class="col-md-9 col-lg-10 content">
        <!-- Header Section -->
        <div class="header-section text-secondary p-4 rounded mb-4">
            <h1 class="text-center mb-0"> Track Requests</h1>
            <p class="text-center">Track all ad requests sent to you by sponsors.</p>
        </div>

        <!-- Ad Requests Table -->
        <div class="table-responsive">
            <table class="table table-bordered table-hover shadow-sm">
                <thead class="table-light">
                    <tr>
                        <th>#</th>
                        <th>Campaign Title</th>
                        <th>Sponsor</th>
                        <th>Sent By</th>
                        <th>Payment Offered</th>
                        <th>Status</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in allData" :key="request.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ request.CampName }}</td>
                        <td>{{ request.SpoName }}</td>
                        <td v-if="request.type === 'sponsor_initiated'">
                            {{request.SpoName}} Sent</td>
                        <td v-else>
                            You Sent</td>
                        <td>${{ request.payment_amount }}</td>

                        
                        <td>
                            <span v-if="request.status != 'Negotiating'" class="badge"
                                :class="{
                                    'bg-success': request.status === 'Accepted',
                                    'bg-danger': request.status === 'Rejected',
                                    'bg-warning': request.status === 'Pending',
                                    'bg-info': request.status === 'Negotiating',
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
            allData: [],
        };
    },

    created() {
        this.fetchAdRequests();
    },

    methods: {
        fetchAdRequests() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/allrequests', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + local.token,
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => {
                    if (response.status === 401) {
                        router.push('/login');
                    } else if (!response.ok) {
                        alert('Failed to fetch ad requests.');
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data) {
                        console.log(data);
                        this.allData = data.request.slice().reverse();
                    }
                })
                .catch((error) => console.error("Error fetching ad requests:", error));
        },

        // respondToRequest(id, action) {
        //     const confirmation = confirm(`Are you sure you want to ${action.toLowerCase()} this request?`);
        //     if (!confirmation) return;

        //     const local = JSON.parse(localStorage.getItem("user"));
        //     fetch(import.meta.env.VITE_BASEURL + '/respondrequest', {
        //         method: 'POST',
        //         headers: {
        //             'Authorization': 'Bearer ' + local.token,
        //             'Content-Type': 'application/json',
        //         },
        //         body: JSON.stringify({ id, action }),
        //     })
        //         .then((response) => response.json())
        //         .then((data) => {
        //             if (data.success) {
        //                 alert(`Request ${action.toLowerCase()}ed successfully.`);
        //                 this.fetchAdRequests();
        //             } else {
        //                 alert('Failed to process the request.');
        //             }
        //         })
        //         .catch((error) => console.error("Error responding to request:", error));
        // },

        Negotiate(id) {
            router.push({ name: 'InfNegotiation', params: { id: id } });
     },
    },
};
</script>

<style scoped>
.header-section {
    text-align: center;
    border-radius: 8px;
    margin-bottom: 20px;
    
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



.btn {
    font-size: 0.85rem;
    padding: 5px 10px;
}
</style>
