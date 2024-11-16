<template>
    <!-- Main Content -->
    <div class="content p-5">
        <h1 class="text-center mb-5">Welcome to Your Dashboard</h1>
        <p class="text-center lead">As a Sponsor, you can manage your campaigns, search for influencers, and track your
            requests here.</p>

            <!-- Quick Stats Section -->
            <div class="row text-center mb-4">
            <div class="col-md-4">
                <div class="card stats-card shadow" style="min-height:88pt ;">
                    <div class="card-body">
                        <h5 class="card-title text-info">Total Budget</h5>
                        <p class="card-text">
                            <strong class="text-success h5 fw-bolder" >$ {{ sponsor.Budget || 0 }}</strong>
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stats-card shadow">
                    <div class="card-body">
                        <h5 class="card-title text-primary">Active Campaigns</h5>
                        <p><strong class="text-success h4 fw-bolder" >{{sponsor.active_camp}}</strong></p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stats-card shadow">
                    <div class="card-body">
                        <h5 class="card-title text-warning">Pending Requests</h5>
                        <p><strong class="text-success h4 fw-bolder" >{{sponsor.active_camp}}</strong></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Profile Section -->
        <h3 class="mt-5 mb-3 text-primary">Your Profile</h3>
        <div class="card profile-card shadow-lg">
            <div class="profile-header">
                <h4 class="text-center">{{ sponsor.name }}</h4>
                <p class="text-muted text-center">{{ sponsor.Cname }}</p>
            </div>
            <div class="card-body">
                <p><strong>Email:</strong> {{ sponsor.email }}</p>
                <p><strong>Company Name:</strong> {{ sponsor.Cname }}</p>
                <p><strong>Industry:</strong> {{ sponsor.Industry }}</p>
                <p><strong>Budget:</strong> $ {{ sponsor.Budget }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 2rem;
}

.text-center {
    color: #343a40;
}

.stats-card {
    background-color: #ffffff;
    border-radius: 10px;
    transition: transform 0.2s;
}

.stats-card:hover {
    transform: scale(1.05);
}

.profile-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
}

.card-title {
    font-weight: bold;
}

.card-text {
    color: #6c757d;
    font-size: 1.1rem;
}

h3 {
    font-weight: 600;
}

p {
    font-size: 1rem;
    color: #495057;
}
</style>



<script>

import router from '@/router';

export default {
    data() {
        return {
            sponsor: [],
        };
    },

    created() {
        this.fetchSponsorData();
    },

    methods: {
        fetchSponsorData() {
            const local = JSON.parse(localStorage.getItem("user"));
            console.log(local.token)
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/' + local.user_id,
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
                    return response.json();
                })
                .then(data => {
                    if (data) {
                        console.log(data);
                        this.sponsor = data;
                    }
                })
                .catch(error => console.error("Error fetching influencer data:", error));
        }
    }

}
</script>
