
<template>
    <div class="content">
        <div class="container campaign-container">
            <h3 class="text-center mb-4">My Campaigns</h3>


            <div v-for="(campaign, index) in campaigns" :key="index" class="campaign-card">
                <h5>Title: {{ campaign.name }}</h5>
                <p><strong>Details:</strong> {{ campaign.description }}</p>
                <p><strong>Goals:</strong> {{ campaign.goals }}</p>
                <p><strong>Category:</strong> {{ campaign.category }}</p>
                <p><strong>Budget:</strong> {{ campaign.budget }}</p>
                <p><strong>Starting Date:</strong> {{ campaign.start_date }}</p>
                <p><strong>Ending Date:</strong> {{ campaign.end_date }}</p>
                <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>

                <div class="d-flex justify-content-between mt-2">
                    <button class="btn btn-warning btn-sm" @click="updateCampaign(campaign.id)">Update</button>
                    <button class="btn btn-danger btn-sm" @click="deleteCampaign(campaign.id)">Delete</button>
                    
                    <button class="btn btn-info btn-sm" @click="checkRequest(campaign.id, campaign.name)">Check Ad Request
                        Status</button>
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
            campaigns: [],
            user: [],
        }
    },

    created() {
        this.fetchCampData();
    },

    methods: {
        fetchCampData() {
            const local = JSON.parse(localStorage.getItem("user"));
            console.log(local.token)
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/campaigns',
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
                        this.campaigns = data.slice().reverse();;
                    }
                })
                .catch(error => console.error("Error fetching influencer data:", error));
        },

        updateCampaign(campaignId) {
            this.$router.push({ name: 'UpdateCampaign', params: { id: campaignId } });
        },

        deleteCampaign(camp_id) {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/CampDelete/' + camp_id,
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': 'Bearer ' + local.token,
                        'Content-Type': 'application/json',
                    },

                }).then(response => {
                    if (response.status == 401) {
                        router.push('/login')
                    }
                    alert('Campaign deleted successfully');
                    this.fetchCampData();
                }).catch(error => console.error("Error deleting campaign:", error));
        },

        checkRequest(camp_id,name) {
            this.$router.push({ name: 'Request', params: { id: camp_id, name:name } });
        },
    }

}
</script>







<style scoped>
.campaign-card {
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #f8f9fa;
}

.campaign-card h5 {
    margin-bottom: 10px;
    color: #007bff;

}

.campaign-card p {
    margin-bottom: 3px;
}

.btn {
    font-size: 0.9rem;
    transition: background-color 0.4s color 0.9s;
}

.btn-warning:hover {
    background-color: #ecaa1a;
    color: white;
}

.btn-danger:hover {
    background-color: #e60000;
    color: black;
}

.btn-info:hover {
    background-color: #17a2b8;
    color: white;
}
</style>v