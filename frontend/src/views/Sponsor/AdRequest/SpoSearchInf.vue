<template>
    <div class="content">
        <div class="container mb-4">
            <h3 class="text-center mb-4">Search Influencer</h3>

            <div class="d-flex align-items-center justify-content-between mb-4 search-bar">
                <input type="text" class="form-control me-2" v-model="name" placeholder="Search by Name"
                    @input="fetchFilteredInfluencers" />

                <select class="form-select me-2" v-model="selectedCategory" @change="fetchFilteredInfluencers">
                    <option value="">Select Category</option>
                    <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
                </select>

                <select class="form-select" v-model="selectedFollowers" @change="fetchFilteredInfluencers">
                    <option value="">Select Followers</option>
                    <option value="1000">1,000+</option>
                    <option value="10000">10,000+</option>
                    <option value="50000">50,000+</option>
                    <option value="100000">100,000+</option>
                </select>
            </div>



            <div v-if="influencers.length > 0" class="influencer-list">
                <div v-for="(influencer, index) in influencers" :key="index" class="influencer-card me-5">
                    <h5>{{ influencer.name }}</h5>
                    <p><strong>Email:</strong> {{ influencer.email }}</p>
                    <p><strong>Followers:</strong> {{ influencer.followers }}</p>
                    <p><strong>Category:</strong> {{ influencer.category }}</p>
                    <p><strong>Niche:</strong> {{ influencer.niche }}</p>
                    <p><strong>Bio:</strong> {{ influencer.bio }}</p>

                    <!-- Button to open modal -->
                    <button class="btn btn-primary btn-sm mt-3" @click="openRequestModal(influencer.id)">
                        Send Request
                    </button>
                </div>
            </div>

            <p v-else class="text-center">No influencers found matching your criteria.</p>

            <!-- Request Modal -->
            <div class="modal" :style="{ display: (show) ? 'block' : 'none' }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="sendRequestModalLabel">Send Request {{ selectedInfluencerId }}
                            </h5>
                            <button type="button" class="btn-close" @click="show = false" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <div class="modal-body">
                            <form @submit.prevent="sendRequest">
                                <div class="mb-3">
                                    <label for="campi" class="form-label">Select Campaign to send Request</label>
                                    <select class="form-select" id="campi" v-model="selectedCampaign">
                                        <option value="">Select Campaign</option>
                                        <option v-for="camp in campaigns" :key="camp" :value="camp.id">{{ camp.name }}</option>
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label for="message" class="form-label">Message</label>
                                    <textarea id="message" v-model="requestMessage" class="form-control"
                                        placeholder="Type your message"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label for="requirements" class="form-label">Requirements</label>
                                    <input type="text" id="requirements" v-model="requestRequirements"
                                        class="form-control" placeholder="Specify any requirements">
                                </div>
                                <div class="mb-3">
                                    <label for="payment" class="form-label">Proposed Payment</label>
                                    <input type="number" id="payment" v-model="requestPayment" class="form-control"
                                        placeholder="Enter amount">
                                </div>
                                <button type="submit" class="btn btn-success">Send</button>
                            </form>
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
            name: "",
            selectedCategory: "",
            selectedFollowers: "",
            influencers: [],
            categories: ["Technology", "Fashion", "Health", "Food", "Travel"], // Replace with categories from backend if needed

            campaigns: [],
            selectedInfluencerId: null,
            requestMessage: '',
            requestRequirements: '',
            requestPayment: '',
            show: false,
            selectedCampaign: '',
        };
    },
    methods: {
        fetchFilteredInfluencers() {
            const local = JSON.parse(localStorage.getItem("user"));

            const queryParams = new URLSearchParams({
                name: this.name,
                category: this.selectedCategory,
                followers: this.selectedFollowers,
            }).toString();
        
            fetch(import.meta.env.VITE_BASEURL+'/influencers/search?'+ queryParams, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + local.token,
                    "Content-Type": "application/json",
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    this.influencers = data;
                })
                .catch((error) => console.error("Error fetching influencers:", error));
        },

        openRequestModal(influencerId) {
            this.show = true;
            this.selectedInfluencerId = influencerId;
        },

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
                        this.campaigns = data;
                    }
                })
                .catch(error => console.error("Error fetching influencer data:", error));
        },

        sendRequest() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(`${import.meta.env.VITE_BASEURL}/sponsor/request`, {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + local.token,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    influencer_id: this.selectedInfluencerId,
                    campaign_id: this.selectedCampaign,
                    message: this.requestMessage,
                    requirements: this.requestRequirements,
                    payment: this.requestPayment,
                }),
            })
                .then((response) =>{
                    this.show = false;
                    if(response.status == 201){
                        alert('Request Sended Successfully');
                    }
                    else{
                        alert('Something went Wrong..');
                    }
                })
                .catch((error) => console.error("Error sending request:", error));
        },
    },
    
    created() {
        this.fetchFilteredInfluencers(); // Fetch all influencers initially or load with default filter
        this.fetchCampData();
    },
};
</script>

<style scoped>
.influencer-card {
    width: 100%;
    max-width: 300px;
    padding: 20px;
    border-radius: 10px;
    background-color: #e9e6e6;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
}

.influencer-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
}

.influencer-card h5 {
    margin-bottom: 10px;
    color: #007bff;
}

.search-bar {
    display: flex;
    gap: 10px;
    flex-wrap: nowrap;
}


.influencer-card:hover {
    transform: scale(1.015);
}

p {
    font-size: 1rem;
    color: #495057;
    margin-left: 2px;
    margin-bottom: 3px;
}

.modal-dialog {
    margin: 10% auto;
    width: 50%;
}


.modal {
    background-color: rgba(0, 0, 0, 0.4);

}
</style>
