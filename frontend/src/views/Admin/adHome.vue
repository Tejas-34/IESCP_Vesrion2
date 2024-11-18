<template>
    <div class="content">
        <!-- Main Content -->
        <div class="main-content">
            <!-- Header -->
            <h1 class="text-center mb-5">Welcome to Your Dashboard</h1>

            <!-- Quick Stats -->

            <div class="row text-center mb-5">
                <div class="col-md-3">
                    <div class="card stats-card shadow">
                        <div class="card-body">
                            <h5 class="card-title text-info">Active Users</h5>
                            <p><strong class="text-success h4 fw-bolder">{{ stats.activeUsers }} </strong></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card shadow">
                        <div class="card-body">
                            <h5 class="card-title text-primary">Active Campaigns</h5>
                            <p><strong class="text-success h4 fw-bolder">{{ stats.activeCampaigns }} </strong></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card shadow">
                        <div class="card-body">
                            <h5 class="card-title text-warning">Pending Approvals</h5>
                            <p><strong class="text-success h4 fw-bolder">{{ stats.pendingApprovals }}</strong></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card shadow">
                        <div class="card-body">
                            <h5 class="card-title text-danger">Flagged Content</h5>
                            <p><strong class="text-success h4 fw-bolder">{{ stats.flaggedContent }}</strong></p>
                        </div>
                    </div>
                </div>
            </div>


            <!-- Tables Section -->
            <section class="tables-section">
                <h2>Sponsor Approvals</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Company</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="spo in spoAprov" :key="spo.nam">
                            <td>{{spo.name}}</td>
                            <td>{{ spo.email }}</td>
                            <td>{{ spo.company_name }}</td>
                            <td v-if="spo.pending === true">
                                <button class="btn btn-primary me-1" @click="openView(spo)">View</button>
                                <button class="btn btn-success me-1" @click="handleAction(spo.spo_id,1)">Approve</button>
                                <button class="btn btn-danger me-1" @click="handleAction(spo.spo_id,0)">Deny</button>
                            </td>
                            <td v-else>
                                
                                <span v-if="spo.approve" class="badge bg-success text-light">Approved</span>
                                <span v-else class="badge bg-danger text-light">Deniend</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>



            <!-- model for view -->
            <div class="modal" :style="{ display: (show) ? 'block' : 'none' }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="ViewModalLabel">{{ selectedSponsor.name }}
                            </h5>
                            <button type="button" class="btn-close" @click="show = false" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <div class="modal-body">

                            <p><strong>Username: </strong> {{ selectedSponsor.username }}</p>
                            <p><strong>Name: </strong> {{ selectedSponsor.name }}</p>
                            <p><strong>Email: </strong>{{ selectedSponsor.email }} </p>
                            <p><strong>Comapny Name: </strong> {{ selectedSponsor.company_name }}</p>
                            <p><strong>Industry: </strong>{{ selectedSponsor.industry }}</p>
                            <p><strong>Budget: </strong> {{ selectedSponsor.budget }}</p>

                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>


<script>
export default {
    data() {
        return {
            stats: {
                activeUsers: 0,
                activeCampaigns: 0,
                pendingApprovals: 0,
                flaggedContent: 0,
            },

            spoAprov:[],
            show:false,
            selectedSponsor: [],


        };
    },

    created(){
        this.fetchData();
    },

    methods:{
        fetchData() {
            
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/admin/home',
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
                        this.stats.activeUsers = data.activUser;
                        this.stats.activeCampaigns = data.activeCamp;
                        this.stats.flaggedContent = data.flag;
                        this.stats.pendingApprovals = data.pendingApprove
                        
                        this.spoAprov = data.data.slice().reverse();

                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));


        },

        openView(spo){
            this.show = true;
            this.selectedSponsor = spo;
        },

        handleAction(id,action){
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/admin/approve/' +id+'/'+action, {
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
                        if(action==1){
                            alert('Sponsor has been approved');
                        }
                        else{
                            alert('Sponsor has been denied');
                        }
                        this.fetchData();
                    }
                })

        }
    }
};

</script>


<style scoped>


.stats-card h3 {
    margin-bottom: 1rem;
}

.tables-section table {
    width: 100%;
    border-collapse: collapse;
}

.tables-section th,
.tables-section td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    text-align: left;
}

.tables-section th {
    background: #f8f9fa;
}

.stats-card {
    background-color: #ffffff;
    border-radius: 10px;
    transition: transform 0.2s;
}



.stats-card:hover {
    transform: scale(1.05);
}

.modal {
    background-color: rgba(0, 0, 0, 0.4);

}

.modal-dialog {
    margin: 10% auto;
    width: 50%;
}
</style>
