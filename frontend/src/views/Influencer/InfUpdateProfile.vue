<template>
    <div class="col-md-9 col-lg-10 content">
        <h1 class="mb-4">Update Profile</h1>

        <!-- Update Profile Form -->
        <div class="card">
            <div class="card-body">
                <form @submit.prevent="update">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" v-model="influencer.name">
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" v-model="influencer.username">
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" v-model="influencer.email">
                    </div>
                    <div class="mb-3">
                        <label for="reach" class="form-label">Reach</label>
                        <input type="text" class="form-control" id="reach" v-model="influencer.Reach">
                    </div>
                    <div class="mb-3">
                        <label for="category" class="form-label">Category</label>
                        <select id="category" class="form-select" v-model="influencer.Category">
                            <option selected>Select Category</option>
                            <option value="Lifestyle">Lifestyle</option>
                            <option value="Technology">Technology</option>
                            <option value="Fashion">Fashion</option>
                            <option value="Travel">Travel</option>
                            <option value="Food">Food</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="niche" class="form-label">Niche</label>
                        <input type="text" class="form-control" id="niche" v-model="influencer.Niche">
                    </div>
                    <div class="mb-3">
                        <label for="bio" class="form-label">Bio</label>
                        <textarea class="form-control" id="bio" rows="3" v-model="influencer.bio"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </form>
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
        };
    },

    created() {
        this.fetchInfluencerData();
    },

    methods: {
        fetchInfluencerData() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/' + local.user_id,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + local.token, // Include token in header
                        'Content-Type': 'application/json',
                    },

                }).then(response => {
                    if (!response.status == 200) {
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

        update() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/update',
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + local.token, // Include token in header
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.influencer)
                }).then(response => {
                    if (response.status == 200) {
                        alert('Profile Updated Successfully');
                    }
                })
        }
    }
}
</script>
