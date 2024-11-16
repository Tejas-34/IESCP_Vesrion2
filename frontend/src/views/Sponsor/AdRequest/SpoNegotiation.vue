<template>
    <div class="container mt-5 content">
        <h3 class="text-center mb-4">Negotiation Details</h3>
        
        <div class="card">
            <div class="card-header">
                <h5>Campaign: {{ request.campaign_name }}</h5>
                <p>Sponsor: {{ request.sponsor_name }} | Influencer: {{ request.influencer_name }}</p>
            </div>
            <div class="card-body">
                <div id="message-history" class="mb-3" v-for="(msg,index) in message" :key="index" >

                    <!-- Example Message from Sponsor -->
                    <div v-if="msg.role=='sponsor'" class="alert alert-secondary d-flex justify-content-between">
                        <div>
                            <strong>Sponsor:</strong> {{msg.message}}
                        </div>
                        <span class="text-muted small">{{ msg.timestamp }}</span>
                    </div>

                    <!-- Example Message from Influencer -->
                    <div v-else class="alert alert-info d-flex justify-content-between">
                        <div>
                            <strong>Influencer:</strong> {{ msg.message }}
                        </div>
                        <span class="text-muted small">{{ msg.timestamp }}</span>
                    </div>

                </div>


                <form @submit.prevent="sendMessage">
                    <div class="form-group">
                        <label for="newMessage">Enter your message:</label>
                        <textarea class="form-control" id="newMessage" name="message" v-model="sendMsg" rows="3" required></textarea>
                    </div>
                    <button type="submit"  class="btn btn-success mt-2">Send Message</button>
                </form>

                <hr>
                <div class="d-flex justify-content-between">
                        <button type="submit" class="btn btn-primary">Accept</button>
                        <button type="submit" class="btn btn-danger">Reject</button>
                    
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
            requestId:null,
            request: [],
            message: [],
            sendMsg: null,
        }
    },
    created(){
        this.requestId=this.$route.params.id;
        this.fetchNegotiationDetails();
        console.log(this.requestId);
    },

    mounted(){
        this.fetchNegotiationDetails();
        setInterval(this.fetchNegotiationDetails, 1000);
    },

    methods: {
        fetchNegotiationDetails(){
            // Fetch data from backen
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/request/' + this.requestId,
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
                        this.request = data;
                        this.message = data.messages;
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        sendMessage(){
            const local = JSON.parse(localStorage.getItem("user"));

            fetch(import.meta.env.VITE_BASEURL + '/ad_request/add_message/' + this.requestId,
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + local.token,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: this.sendMsg
                    })
                }).then(response => {
                    if (response.status == 401) {
                        router.push('/login')
                    }
                    else if(!response.status == 200){
                        alert('Something went wrong...');
                    }
                    else{
                        this.sendMsg = null;
                        this.fetchNegotiationDetails();
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
    
        }
    }
}

</script>



<style scoped>
    .alert-info{
        background-color: #d1ecf1;
        color: #31808e;
        border:none;
    }

    .alert-secondary{
        background-color: #e2e3e5;
        color: #353d44;
        border:none;
    }
</style>