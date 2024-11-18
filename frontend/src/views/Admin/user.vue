<template>
    <div class="content">
        <h1 class="text-center">User Management</h1>

        <div class="chart-row">
            <!-- Active Users vs. Flagged Users -->
            <div class="chart-container">
                <h3 style="margin-top:50pt;">Active Users vs. Flagged Users</h3>
                <canvas id="activeUsersChart"></canvas>
            </div>

            <!-- Sponsors vs. Influencers -->
            <div class="chart-container ms-5">
                <h3 style="margin-top:100pt;">Sponsors vs. Influencers</h3>
                <canvas id="userTypesChart"></canvas>
            </div>
        </div>

        <!-- Toggle Button -->
        <div class="d-flex justify-content-center my-3">
            <button class="btn mx-2" :class="{ active: showInfluencers }" @click="toggleView('influencer')">
                Show Influencers
            </button>
            <button class="btn mx-2" :class="{ active: !showInfluencers }" @click="toggleView('sponsor')">
                Show Sponsors
            </button>
        </div>





        <!-- User Table -->
        <table class="table table-striped table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th v-if="showInfluencers">Category</th>
                    <th v-else>Company</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(user, index) in filteredUsers" :key="user.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ showInfluencers ? user.category : user.company_name }}</td>
                    <td>
                        <button v-if="user.flag==false" class="btn btn-warning btn-sm mx-1" @click="flagUser(user.id)">Flag</button>
                        <button v-else  class="btn btn-success btn-sm mx-1" @click="flagUser(user.id)">Unflag</button>
                        <button class="btn btn-danger btn-sm mx-1" @click="deleteUser(user.id)">Delete</button>
                        <button class="btn btn-info btn-sm mx-1" @click="openView(user)">View</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="modal" :style="{ display: (show) ? 'block' : 'none' }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="ViewModalLabel">{{ selectedUser.name }}
                            </h5>
                            <button type="button" class="btn-close" @click="show=false" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <div class="modal-body">

                            <p><strong>Username: </strong> {{ selectedUser.username }}</p>
                            <p><strong>Name: </strong> {{ selectedUser.name }}</p>
                            <p><strong>Email: </strong>{{ selectedUser.email }} </p>
                            <p v-if="selectedUser.totalCamp"><strong>Total Campaign: </strong>{{ selectedUser.totalCamp }} </p>
                            <p v-if="selectedUser.budget"><strong>Budget remaining: </strong>{{ selectedUser.budget }} </p>
                            <p v-if="selectedUser.earning"><strong>Total Earning: </strong>{{ selectedUser.earning }} </p>
                            <p v-if="selectedUser.company_name"><strong>Company Name: </strong>{{ selectedUser.company_name }} </p>
                            <p v-if="selectedUser.industry"><strong>Industry: </strong>{{ selectedUser.industry }} </p>
                            <p v-if="selectedUser.category"><strong>Category: </strong>{{ selectedUser.category }} </p>
                            

                        </div>
                    </div>
                </div>
            </div>

    </div>




</template>

<script>
import Chart from "chart.js/auto";
import router from "@/router";

export default {

    data() {
        return {
            showInfluencers: true, // Toggle state
            influencers: [],
            sponsors: [],
            selectedUser:[],

            show:false,

            activeUsers: 0,
            flaggedUsers: 0,
            sponsorsCount: 0,
            influencersCount: 0,
        }
    },
    mounted() {
        this.fetchData();
    },

    computed: {
        filteredUsers() {
            return this.showInfluencers ? this.influencers : this.sponsors;
        },
    },

    methods: {

        openView(user){
            this.show = true;
            this.selectedUser = user;
        },

        fetchData() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/admin/stats', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + local.token,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (response.status == 401) {
                        router.push('/login');
                    } else if (!response.ok) {
                        alert('Something went wrong...');
                    }
                    return response.json() || {};
                })
                .then(data => {
                    if (data) {
                        this.sponsors = data.sponsor;
                        this.influencers = data.influencers;
                        this.activeUsers = data.activUser;
                        this.flaggedUsers = data.flaggedUsers;
                        this.sponsorsCount = data.sponsorsCount;
                        this.influencersCount = data.influencersCount;

                        // Initialize charts after data is updated
                        this.initializeCharts();
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        initializeCharts() {
            // Active Users Chart
            const ctx1 = document.getElementById("activeUsersChart").getContext("2d");
            new Chart(ctx1, {
                type: "pie",
                data: {
                    labels: ["Active Users", "Flagged Users"],
                    datasets: [
                        {
                            data: [this.activeUsers, this.flaggedUsers],
                            backgroundColor: ["#28a745", "#dc3545"],
                            borderColor: ["#28a745", "#dc3545"],
                            borderWidth: 1,
                        },
                    ],
                },
            });

            // Sponsors vs Influencers Chart
            const ctx2 = document.getElementById("userTypesChart").getContext("2d");
            new Chart(ctx2, {
                type: "bar",
                data: {
                    labels: ["Sponsors", "Influencers"],
                    datasets: [
                        {
                            label: "Count",
                            data: [this.sponsorsCount, this.influencersCount],
                            backgroundColor: ["#007bff", "#fd7e14"],
                            borderColor: ["#007bff", "#fd7e14"],
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                    },
                    scales: {
                        y: { beginAtZero: true },
                    },
                },
            })
        },


        toggleView(type) {
            this.showInfluencers = type === "influencer";
        },

        flagUser(userId) {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/admin/flag/' +userId, {
                method: 'PUT',
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
                    else {
                        alert('Flagging user with ID: '+ userId);
                        this.fetchData();
                        this.initializeCharts();
                    }
                })
        },

        deleteUser(userId) {
            if (confirm("Are you sure you want to delete this user?")) {
                const local = JSON.parse(localStorage.getItem("user"));
                fetch(import.meta.env.VITE_BASEURL + '/admin/delete/' + userId,
                    {
                        method: 'DELETE',
                        headers: {
                            'Authorization': 'Bearer ' + local.token, // Include token in header
                            'Content-Type': 'application/json',
                        },
                    }).then(response => {
                        if (response.status == 401) {
                            router.push('/login')
                        }
                        else if(!response.status == 200){
                            alert('Something went wrong...');
                        }
                        else{
                            alert("User deleted successfully.");
                            this.fetchData();
                        }
                    })
                    .catch(error => console.error("Error fetching campaign data:", error));
                
            }
        },

        viewUser(userId) {
            alert(`Viewing details for user with ID: ${userId}`);
        },
    },
}

</script>


<style scoped>
.chart-row {
    display: flex;
    justify-content: space - between;
    flex-wrap: wrap;
}

#activeUsersChart {
    width: 300px;
}

#userTypesChart {
    width: 500px;
    height: 800px;
}

@media(max-width: 300px) {
    .chart-container {
        flex: 1 1 100%;
        /* One chart per row on smaller screens */
        max-width: 100%;
    }
}


.active {
    font-weight: bold;
    border: 2px solid #007bff;
}

.table th,
.table td {
    text-align: center;
    vertical-align: middle;
}

.modal {
    background-color: rgba(0, 0, 0, 0.4);

}

.modal-dialog {
    margin: 10% auto;
    width: 50%;
}
</style>
