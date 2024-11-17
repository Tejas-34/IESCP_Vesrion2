<template>
    <div class="content">
        <div class="container mb-4">
            <h3 class="text-center mb-4">Search Campaign</h3>

            <div class="d-flex align-items-center justify-content-between mb-4 search-bar">
                <input type="text" class="form-control me-2" v-model="name" placeholder="Search by Name"
                    @input="fetchFilteredCampaigns" />

                <select class="form-select me-2" v-model="selectedCategory" @change="fetchFilteredCampaigns">
                    <option value="">Select Category</option>
                    <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
                </select>

                <select class="form-select" v-model="selectedBudget" @change="fetchFilteredCampaigns">
                    <option value="">Select Budget</option>
                    <option value="100">$100+</option>
                    <option value="1000">$1000+</option>
                    <option value="5000">$5000+</option>
                    <option value="10000">$10000+</option>
                </select>
            </div>



            <div v-if="campaigns.length > 0" class="influencer-list">
                <div v-for="(campaign, index) in campaigns" :key="index" class="influencer-card me-5">
                    <h5>Title: {{ campaign.name }}</h5>
                <p><strong>Details:</strong> {{ campaign.description }}</p>
                <p><strong>Goals:</strong> {{ campaign.goals }}</p>
                <p><strong>Category:</strong> {{ campaign.category }}</p>
                <p><strong>Budget:</strong> {{ campaign.budget }}</p>
                <p><strong>Starting Date:</strong> {{ campaign.start_date }}</p>
                <p><strong>Ending Date:</strong> {{ campaign.end_date }}</p>

                    <!-- Button to open modal -->
                    <button class="btn btn-primary btn-sm mt-3" @click="openRequestModal(campaign.id, campaign.sponsor_id)">
                        Send Request
                    </button>
                </div>
            </div>

            <p v-else class="text-center">No Campaign found matching your criteria.</p>

            <!-- Request Modal -->
            <div class="modal" :style="{ display: (show) ? 'block' : 'none' }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="sendRequestModalLabel">Send Request
                            </h5>
                            <button type="button" class="btn-close" @click="show = false" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <div class="modal-body">
                            <form @submit.prevent="sendRequest">

                                <div class="mb-3">
                                    <label for="payment" class="form-label">Proposed Payment</label>
                                    <input type="number" id="payment" v-model="requestPayment" class="form-control"
                                        placeholder="Enter amount">
                                </div>

                                <div class="mb-3">
                                    <label for="message" class="form-label">Message</label>
                                    <textarea id="message" v-model="requestMessage" class="form-control"
                                        placeholder="Type your message"></textarea>
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
            selectedBudget: "",
            campaigns: [],
            categories: ["Technology", "Fashion", "Health", "Food", "Travel"], // Replace with categories from backend if needed

            
            selectedCampaignId: null,
            selectedSponsorId:null,
            requestMessage: '',
            requestPayment: '',
            show: false,
        };
    },
    methods: {
        fetchFilteredCampaigns() {
            const local = JSON.parse(localStorage.getItem("user"));

            const queryParams = new URLSearchParams({
                name: this.name,
                category: this.selectedCategory,
                budget: this.selectedBudget,
            }).toString();
        
            fetch(import.meta.env.VITE_BASEURL+'/campaigns/search?'+ queryParams, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + local.token,
                    "Content-Type": "application/json",
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    this.campaigns = data;
                    
                })
                .catch((error) => console.error("Error fetching influencers:", error));
        },

        openRequestModal(campaign_id, sponsor_id) {
            this.selectedCampaignId = campaign_id;
            this.selectedSponsorId = sponsor_id;
            this.show = true;
        },

        // fetchCampData() {
        //     const local = JSON.parse(localStorage.getItem("user"));
        //     console.log(local.token)
        //     fetch(import.meta.env.VITE_BASEURL + '/sponsor/campaigns',
        //         {
        //             method: 'GET',
        //             headers: {
        //                 'Authorization': 'Bearer ' + local.token,
        //                 'Content-Type': 'application/json',
        //             },

        //         }).then(response => {
        //             if (response.status == 401) {
        //                 router.push('/login')
        //             }
        //             return response.json();
        //         })
        //         .then(data => {
        //             if (data) {
        //                 console.log(data);
        //                 this.campaigns = data;
        //             }
        //         })
        //         .catch(error => console.error("Error fetching influencer data:", error));
        // },

        sendRequest() {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL+ '/influencer/request', {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + local.token,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    sponsor_id: this.selectedSponsorId,
                    campaign_id: this.selectedCampaignId,
                    message: this.requestMessage,
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
        this.fetchFilteredCampaigns(); // Fetch all influencers initially or load with default filter
    },
};
</script>

<style scoped>
.influencer-card {
    width: 100%;
    max-width: 300px;
    padding: 20px;
    border-radius: 10px;
    background-color: #f2f5ee;
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
    color: #0a5353;
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
