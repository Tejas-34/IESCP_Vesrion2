<template>
  <div class="col-md-9 col-lg-10 content">
                <h1 class="mb-4" align="center">Update Profile</h1>
                <!-- Update Profile Form -->
                <div>
                    <div >
                        <form @submit.prevent="update">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" v-model="sponsor.name">
                            </div>
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" class="form-control" id="username" v-model="sponsor.username">
                            </div>

                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" v-model="sponsor.email">
                            </div>
                            <div class="mb-3">
                                <label for="cname" class="form-label">Company Name</label>
                                <input type="text" class="form-control" id="cname" v-model="sponsor.Cname" >
                            </div>
                            <div class="mb-3">
                                <label for="budget" class="form-label">Budget</label>
                                <input type="text" class="form-control" id="budget" v-model="sponsor.Budget">
                            </div>
                            <div class="mb-3">
                                <label for="industry" class="form-label">Industry</label>
                                <input type="text" class="form-control" id="industry" v-model="sponsor.Industry">
                            </div>
                            <div class="mb-3">
                                <label for="bio" class="form-label">Bio</label>
                                <textarea class="form-control" id="bio" rows="3" v-model="sponsor.bio"></textarea>
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
                        this.sponsor = data;
                    }
                })
                .catch(error => console.error("Error fetching influencer data:", error));
        },

        update() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/update',
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + local.token, // Include token in header
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.sponsor)
                }).then(response => {
                    if (response.status == 200) {
                        alert('Profile Updated Successfully');
                    }
                })
        }
    }

}
</script>

