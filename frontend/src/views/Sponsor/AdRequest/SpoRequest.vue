<template>
    <div class="container content py-4">
        <h3 class="text-center text-primary"> Campaign Requests</h3>
        <h3 class="text-center mb-5 text-success"> {{ campaignName }}</h3>
        
        <div class="row g-4">
    
            <!-- Additional Campaign Cards can be added here -->
             
            <div class="col-md-6" v-for="(request, index) in requests" :key="index" >
                <div class="card border-0 rounded-lg shadow p-3 mb-5 bg-body rounded">

                    <div class="card-header bg-warning text-dark d-flex justify-content-between align-items-center" :style="{ display: (request.status=='Pending') ? 'block' : 'none' }"> 
                        <h5 class="card-title mb-0">{{request.name}}</h5>
                        <span class="badge bg-secondary" :style="{ display: (request.status=='Pending') ? 'block' : 'none' }"> {{ request.status }}  </span>
                        <span class="badge bg-danger" :style="{ display: (request.status=='Rejected') ? 'block' : 'none' }" > Rejected </span>
                        <span class="badge bg-success" :style="{ display: (request.status=='Accepted') ? 'block' : 'none' }" > Accepted  </span>
                        <span class="badge bg-info" :style="{ display: (request.status=='Negotiating') ? 'block' : 'none' }" > Negotiating  </span>
                    </div>

                    <div class="card-body ">
                        <p><strong>Email:</strong> <span class="text-secondary">{{request.email}}</span></p>
                        <p><strong>Payment Amount:</strong> <span class="text-success">${{request.payment_amount}}</span></p>
                        <p><strong>Requirements:</strong> <span class="text-secondary">{{request.requirements}}</span></p>
                    </div>
                    <div class="card-footer bg-white d-flex justify-content-between">
                        <button type="button" @click="update(request.id, request.requirements, request.payment_amount)" class="btn btn-info btn-sm me-2">Edit</button>
                        <div class="d-flex flex-wrap">
                            <button type="button" @click="deleteReq(request.id)" class="btn btn-danger btn-sm me-2">Delete</button>
                            
                            <button @click="Negotiate(request.id)" class="btn btn-outline-info btn-sm" :style="{ display: (request.status=='Negotiating') ? 'block' : 'none' }" >Continue Negotiation</button>
                        </div>
                    </div>
                </div>
            </div>

            <p align="center" class="text-danger" :style="{ display: (requests.length == 0) ? 'block' : 'none' }" > ..........You don't have made 
                any request till for this campaign............ </p>
           
            
            




            <!-- Edit Request Modal --> 

            <div class="modal" :style="{ display: (show) ? 'block' : 'none' }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="sendRequestModalLabel">Send Request {{ selectedRequest }}
                            </h5>
                            <button type="button" class="btn-close" @click="show = false" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <div class="modal-body">
                            <form @submit.prevent="submit">
                                
                                <div class="mb-3">
                                    <label for="payment" class="form-label"> Payment</label>
                                    <input type="number" id="payment" v-model="selectedPayment" class="form-control"
                                       >
                                </div>

                                <div class="mb-3">
                                    <label for="requirements" class="form-label">Requirements</label>
                                    <textarea type="text" id="requirements" v-model="selectedRequirements"
                                        class="form-control" > </textarea>
                                </div>

                                
                                <button type="submit" class="btn btn-success">Update</button>
                            </form>
                        </div>
                    </div>
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
            campaignId: null,
            campaignName:null,
            requests: [],
            selectedRequest: null,
            selectedPayment: null,
            selectedRequirements: null,
            show: false,

        }
    },

    created(){
        this.campaignId = this.$route.params.id;
        this.campaignName = this.$route.params.name;
        this.fetchReqestData();
        
    },

    methods:{

        fetchReqestData(){
            // Fetch data from backen
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/Sponsor/CampRequests/' + this.campaignId,
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
                        this.requests = data.request;
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
            },

            update(id, requirements, payment){
                // Update request
                console.log('Update request',id);
                this.show = true;
                this.selectedPayment = payment;
                this.selectedRequirements = requirements;
                this.selectedRequest = id;

            },

            submit(){
                console.log('Submit request',this.selectedRequest);
                const local = JSON.parse(localStorage.getItem("user"));
                fetch(import.meta.env.VITE_BASEURL + '/sponsor/request/update/' + this.selectedRequest,
                    {
                        method: 'PUT',
                        headers: {
                            'Authorization': 'Bearer ' + local.token, // Include token in header
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            payment_amount: this.selectedPayment,
                            requirements: this.selectedRequirements
                        })
                    }).then(response => {
                        if (response.status == 401) {
                            router.push('/login')
                        }
                        else if(!response.status == 200){
                            alert('Something went wrong...');
                        }
                        else{
                            alert('Request updated successfully');
                            this.fetchReqestData();
                            this.show = false;
                        }
                    })
                    
                    .catch(error => console.error("Error fetching campaign data:", error));
            },
            
            deleteReq(id){
                // Delete request
                console.log('Delete request',id);
                const local = JSON.parse(localStorage.getItem("user"));
                fetch(import.meta.env.VITE_BASEURL + '/sponsor/request/delete/' + id,
                    {
                        method: 'DELETE',
                        headers: {
                            'Authorization': 'Bearer ' + local.token, // Include token in header
                            'Content-Type': 'application/json',
                        },
                    }).then(response => {
                        if (response.status == 401) {
                            router.push('/login')
                        }
                        else if(!response.status == 200){
                            alert('Something went wrong...');
                        }
                        else{
                            alert('Request deleted successfully');
                            this.fetchReqestData();
                        }
                    })
                    .catch(error => console.error("Error fetching campaign data:", error));
            },

            Negotiate(id){
                this.$router.push({ name: 'SpoNegotiation', params: { id: id } });
            }

        },
}



</script>






<style scoped>
.card-title {
    font-weight: bold;
}

.btn-outline-info {
    background-color: #1888a2;
    color:white;
    border-color: #0dcaf0;
}

.btn-outline-info:hover {
    background-color: #5b7479;
    border-color:#5b7479;
}

.card-body p {
    margin: 0.5rem 0;
}

.modal {
    background-color: rgba(0, 0, 0, 0.4);

}
.modal-dialog {
    margin: 10% auto;
    width: 50%;
}

</style>
