<template>
    <div class="col-md-9 col-lg-10 content">
        <!-- Header -->
        <div class="header-section  p-4 rounded mb-4 shadow-sm">
            <h1 class="mb-0 text-center">Manage Your Ad Requests</h1>
        </div>

        <!-- Ad Request Cards -->
        <div class="ad-request-list">
            <div class="card shadow-sm mb-4" v-for="(request, index) in allData" :key="index">
                <div class="card-header bg-light d-flex justify-content-between align-items-center">
                    <h3 class="card-title mb-0 text-dark">Campaign {{ index + 1 }}: {{ request.CampName }}</h3>
                    <span class="badge" :class="getStatusBadgeClass(request.status)">{{ request.status }}</span>
                </div>
                <div class="card-body">
                    <p><strong>Sponsor Name:</strong> {{ request.SpoName }}</p>
                    <p><strong>Company:</strong> {{ request.CompanyName }}</p>
                    <p><strong>Payment Amount:</strong> ${{ request.payment_amount }}</p>
                    <p><strong>Requirements:</strong> {{ request.requirements }}</p>
                </div>
                <div class="card-footer d-flex justify-content-between align-items-center">
                    <button class="btn btn-primary btn-sm me-2" @click="handleActionView(request.CampName)">
                         View
                    </button>
                    <button class="btn btn-success btn-sm me-2" @click="handleAction('Accepted', request.id)"
                        v-if="request.status === 'Pending'">
                        Accept
                    </button>
                    <button class="btn btn-danger btn-sm me-2" @click="handleAction('Rejected', request.id)"
                        v-if="request.status === 'Pending'">
                        Reject
                    </button>
                    <button class="btn btn-warning btn-sm me-2" @click="handleAction('Negotiating', request.id)"
                        v-if="request.status === 'Pending'">
                        Negotiate
                    </button>
                    <button class="btn btn-info btn-sm me-2" @click="Negotiate(request.id)"
                        v-if="request.status === 'Negotiating'">
                         Continue Negotiation
                    </button>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal" :style="{ display: show ? 'block' : 'none' }">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title ">{{ selected.CampName }}</h5>
                        <button type="button" class="btn-close" @click="show = false" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Budget:</strong> ${{ selected.budget }}</p>
                        <p><strong>Category:</strong> {{ selected.category }}</p>
                        <p><strong>Details:</strong> {{ selected.description }}</p>
                        <p><strong>Goals:</strong> {{ selected.goals }}</p>
                        <p><strong>Starting Date:</strong> {{ selected.start_date }}</p>
                        <p><strong>Ending Date:</strong> {{ selected.end_date }}</p>
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
            allData: [],
            show: false,
            selected: [],
            campaign: [],
        }
    },
    methods: {
        fetchReqestData() {
            // Fetch data from backen
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/requests',
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
                    else if (!response.status == 200) {
                        alert('Something went wrong...');
                    }
                    return response.json() || {};
                })
                .then(data => {
                    if (data) {
                        console.log(data);
                        this.allData = data.combine.slice().reverse();
                        this.campaign = data.campaign.slice().reverse();
                    }
                })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        handleAction(action, id) {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/request/update/' + id, {
                method: 'PUT',
                headers: {
                    'Authorization': 'Bearer ' + local.token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'status': action })
            }).then(response => {
                if (response.status == 401) {
                    router.push('/login')
                }
                else if (!response.status == 200) {
                    alert('Something went wrong...');
                }
                else {
                    alert('request has been ' + action)
                    this.fetchReqestData();

                }
            })
                .catch(error => console.error("Error fetching campaign data:", error));
        },

        handleActionView(CampName) {
            for (let i = 0; i < this.campaign.length; i++) {
                if (this.campaign[i].CampName == CampName) {
                    this.selected = this.campaign[i];
                    console.log(this.selected);
                    this.show = true;
                    break;
                }
            }
        },
        getStatusBadgeClass(status) {
            switch (status) {
                case 'Pending': return 'bg-secondary text-light';
                case 'Rejected': return 'bg-danger text-light';
                case 'Accepted': return 'bg-success text-light';
                case 'Negotiating': return 'bg-info text-dark';
                default: return 'bg-light text-dark';
            }
        },

        Negotiate(id) {
            router.push({ name: 'InfNegotiation', params: { id: id } });
        }

    },


    created() {
        this.fetchReqestData();

    }
}

</script>








<style scoped>
.header-section {
    border-radius: 8px;
    margin-bottom: 1.5rem;
    text-align: center;
}
.header-section {
  border-radius: 8px;
  text-align: center;
  color: darkgoldenrod;
  background-color:aliceblue;
}

.card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  border-radius: 10px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 1.2rem;
}

.card-footer .btn {
  font-size: 0.85rem;
}

.modal-content {
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.modal-header {
    background-color: #007bff;
  color: white;
}

.modal-header .btn-close {
  color: white;
}
.modal {
    background-color: rgba(0, 0, 0, 0.4);

}

</style>
