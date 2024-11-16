<template>
    <div class="content">
        <h2 align="center">Update Campaign</h2>
        <form @submit.prevent="update">
            <div class="form-group mb-2">
                <label for="campaignName">Campaign Name </label>
                <input type="text" class="form-control" name="Name" id="campaignName" 
                    v-model="camp.name" required>
            </div>

            <div class="form-group mb-2">
                <label for="description">Description</label>
                <textarea class="form-control" id="description" name="Description" rows="4"
                    placeholder="Enter campaign description" v-model="camp.description" required></textarea>
            </div>

            <div class="form-group mb-2">
                <label for="startDate">Start Date</label>
                <input type="date" class="form-control" name="Start_date" id="startDate" v-model="camp.start_date"
                    required>
            </div>

            <div class="form-group mb-2">
                <label for="endDate">End Date</label>
                <input type="date" class="form-control" name="End_date" id="endDate" v-model="camp.end_date"
                    required>
            </div>

            <div class="form-group mb-2">
                <label for="budget">Budget</label>
                <input type="number" class="form-control" name="Budget" id="budget" 
                    v-model="camp.budget" required>
            </div>

            <div class="form-group mb-2">
                <label for="visibility">Visibility</label>
                <select class="form-control" name="visibility" id="visibility" v-model="camp.visibility" required>
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                </select>
            </div>

            <div class="form-group mb-2">
                <label for="goals">Goals</label>
                <textarea class="form-control" name="goal" id="goals" rows="3" placeholder="Enter campaign goals"
                    v-model="camp.goals" required></textarea>
            </div>

            <div class="mb-3">
                <label for="category" class="form-label">Category</label>
                <select id="category" class="form-select" v-model="camp['category']">
                    <option>Select Category</option>
                    <option value="Lifestyle">Lifestyle</option>
                    <option value="Technology">Technology</option>
                    <option value="Fashion">Fashion</option>
                    <option value="Travel">Travel</option>
                    <option value="Food">Food</option>
                </select>
            </div>

            <button type="submit" class="btn btn-primary me-3">Save Changes</button>
            <router-link to="/sponsor/Camp" class="btn btn-secondary">Cancel</router-link>
        </form>


    </div>
</template>


<script>

import router from '@/router';

export default {
    data() {
        return {
            camp: [],
            campaignId: null,
        }
    },

    created(){
        this.campaignId = this.$route.params.id;
        this.fetchCampData();
    },

    methods: {
        fetchCampData() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/campaign/' + this.campaignId,
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
                    else if(!response.status == 200){
                        alert('Something went wrong...');
                    }
                    return response.json() || {};
                })
                .then(data => {
                    if (data) {
                        console.log(data);
                        this.camp = data;
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        update() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/CampUpdate/' + this.campaignId,
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + local.token, // Include token in header
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.camp)
                }).then(response => {
                    if (response.status == 200) {
                        alert('Campaign Updated Successfully');
                        router.push('/sponsor/Camp');
                    }
                })
        },
    }
}

</script>






<style scoped>
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