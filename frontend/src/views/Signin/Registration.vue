<template>
    <div class="container-fluid">
        <div class="card row col-md-6 pb-5 login-card mt-3">
            <div class="card-body">
                <div class=" text-center ">
                    <h2>Registration</h2>
                </div>
                <form @submit.prevent="signin">

                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control" placeholder="Name" v-model="name" required>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control" placeholder="Username" v-model="username" required>
                            <div class="invalid-feedback" :style="{ display: (log) ? 'block' : 'none' }">
                                Registration Failed username alrady exits.
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col">
                            <input type="email" class="form-control" placeholder="Email" v-model="email" required>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col">
                            <input type="password" class="form-control" placeholder="Password" v-model="password"
                                required>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col">
                            <label for="bio" class="form-label">Bio</label>
                            <textarea class="form-control" id="bio" rows="3"
                                placeholder="Write a short bio about yourself" v-model="bio"></textarea>
                        </div>
                    </div>


                    <div class="form-group">
                        <label for="roleSelect">Select Role</label>
                        <select class="form-control" id="roleSelect" v-model="selectedRole">
                            <option value="sponsor">Sponsor</option>
                            <option value="influencer">Influencer</option>
                        </select>
                    </div>

                    <!-- Sponsor Section -->
                    <div id="sponsorSection" class="role-section" v-if="selectedRole === 'sponsor'">

                        <div class="row">
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Company Name"
                                    v-model="sponsor['Cmpname']" required>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Industry"
                                    v-model="sponsor['industry']" required>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col">
                                <input type="number" class="form-control" placeholder="Budget"
                                    v-model="sponsor['budget']" required>
                            </div>
                        </div>

                    </div>

                    <!-- Influencer Section -->
                    <div id="influencerSection" class="role-section" v-if="selectedRole === 'influencer'">

                        <div class="row">
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Niche"
                                    v-model="influencer['niche']" required>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col">
                                <input type="text" class="form-control" placeholder="Reach"
                                    v-model="influencer['reach']" required>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="category" class="form-label">Category</label>
                            <select id="category" class="form-select" v-model="influencer['category']">
                                <option selected>Select Category</option>
                                <option value="Lifestyle">Lifestyle</option>
                                <option value="Technology">Technology</option>
                                <option value="Fashion">Fashion</option>
                                <option value="Travel">Travel</option>
                                <option value="Food">Food</option>
                            </select>
                        </div>
                    </div>

                    <div class="mt-3">
                        <input type="submit" class="btn btn-primary">
                    </div>
                </form>

            </div>
            <p>Have a account? <router-link to="/login" align="center">login</router-link></p>
        </div>
    </div>
</template>

<script>

import router from '@/router';

export default {
    data() {
        return {
            name: null,
            username: null,
            password: null,
            email: null,
            bio: null,
            selectedRole: null,
            log: false,

            influencer: {
                niche: null,
                reach: null,
                category: null
            },
            sponsor: {
                budget: null,
                industry: null,
                Cmpname: null
            },
            data: {},
        }
    },
    methods: {
        signin() {
            this.formate(); // Call to set up this.data with the form values
            fetch(import.meta.env.VITE_BASEURL + '/register', {
                method: "POST",
                headers: { 'Content-Type': "application/json" },
                body: JSON.stringify(this.data)
            })
                .then(response => {
                    if (response.status === 201) {
                        return response.json();
                    } else if (response.status === 409) {
                        this.log = true;
                        router.push('/signin');
                        return {};
                    } else {
                        return {};
                    }
                })
                .then(data => {
                    if (data && data.role) {
                        if (data.role === "influencer") {
                            router.push('/signin/suc');
                        } else if (data.role === "sponsor") {
                            router.push('/signin/pending');
                        }
                    }
                })
                .catch(error => console.error("Error during registration:", error));
        },
        formate() {
            if (this.selectedRole === 'influencer') {
                this.data = {
                    name: this.name,
                    email: this.email,
                    username: this.username,
                    password: this.password,
                    bio:this.bio,
                    role: 'influencer',
                    niche: this.influencer['niche'],
                    reach: this.influencer['reach'],
                    category: this.influencer['category']
                }
            }
            else {
                this.data = {
                    name: this.name,
                    email: this.email,
                    username: this.username,
                    password: this.password,
                    bio:this.bio,
                    role: "sponsor",
                    budget: this.sponsor['budget'],
                    industry: this.sponsor['industry'],
                    Cmpname: this.sponsor['Cmpname']

                }
            }
        }
    }
}

</script>





<style scoped>
.container-fluid {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
}

.login-card {
    box-shadow: 0px 0px 20px rgba(0, 0, 0.1);
    border-radius: 8px;
    min-height: 350px;
}

.btn-primary {
    width: 100%;
}

.row {
    padding: 10px 0 10px 0;
}
</style>