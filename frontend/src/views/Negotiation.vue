<template>
    <div class="container mt-5 content">
      <h3 class="text-center mb-4">Negotiation Details</h3>
  
      <div class="card shadow-sm">
        <div class="card-header bg-primary text-white">
          <h5>Campaign: {{ request.campaign_name }}</h5>
          <p class="mb-0">
            <strong>Sponsor:</strong> {{ request.sponsor_name }} |
            <strong>Influencer:</strong> {{ request.influencer_name }}
          </p>
        </div>
        <div class="card-body">
          <div id="message-history" class="mb-3">
            <div
              v-for="(msg, index) in message"
              :key="index"
              :class="[
                'alert',
                'd-flex',
                'justify-content-between',
                msg.role === 'sponsor' ? 'alert-secondary' : 'alert-info',
              ]"
            >
              <div>
                <strong>{{ capitalize(msg.role) }}:</strong> {{ msg.message }}
              </div>
              <span class="text-muted small">{{ formatTimestamp(msg.timestamp) }}</span>
            </div>
          </div>
  
          <form @submit.prevent="sendMessage">
            <div class="form-group">
              <label for="newMessage">Enter your message:</label>
              <textarea
                class="form-control"
                id="newMessage"
                v-model="sendMsg"
                rows="3"
                required
              ></textarea>
            </div>
            <button type="submit" class="btn btn-success mt-2">Send Message</button>
          </form>
  
          <hr />
          <div class="d-flex justify-content-between">
            <button class="btn btn-primary" @click="handleAction('Accepted')">
              Accept
            </button>
            <button class="btn btn-danger" @click="handleAction('Rejected')">
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import router from "@/router";
  
  export default {
    data() {
      return {
        
        requestId: null,
        request: [],
        message: [],
        sendMsg: null,
      };
    },
  
    created() {
      this.requestId = this.$route.params.id;
      this.fetchNegotiationDetails();
    },
  
    mounted() {
      this.fetchNegotiationDetails();
      setInterval(this.fetchNegotiationDetails, 3000);
    },
  
    methods: {
      fetchNegotiationDetails() {
        const local = JSON.parse(localStorage.getItem("user"));
        fetch(`${import.meta.env.VITE_BASEURL}/request/${this.requestId}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${local.token}`,
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (response.status === 401) {
              router.push("/login");
            } else if (response.status !== 200) {
              alert("Something went wrong...");
            }
            return response.json() || {};
          })
          .then((data) => {
            if (data) {
              this.request = data;
              this.message = data.messages;
            }
          })
          .catch((error) =>
            console.error("Error fetching negotiation details:", error)
          );
      },
  
      sendMessage() {
        const local = JSON.parse(localStorage.getItem("user"));
  
        fetch(
          `${import.meta.env.VITE_BASEURL}/ad_request/add_message/${this.requestId}`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${local.token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              message: this.sendMsg,
            }),
          }
        )
          .then((response) => {
            if (response.status === 401) {
              router.push("/login");
            } else if (response.status !== 200) {
              alert("Something went wrong...");
            } else {
              this.sendMsg = null;
              this.fetchNegotiationDetails();
            }
          })
          .catch((error) =>
            console.error("Error sending negotiation message:", error)
          );
      },
  
      handleAction(action) {
            const local = JSON.parse(localStorage.getItem("user"));
            fetch(import.meta.env.VITE_BASEURL + '/influencer/request/update/' + this.requestId, {
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
  
      formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString();
      },
  
      capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
      },
    },
  };
  </script>
  
  <style scoped>

    .content {
        
        justify-content: center;
        margin-left:500px;
    }

  .alert-info {
    background-color: #e3f7fc;
    color: #0275d8;
    border: none;
  }
  
  .alert-secondary {
    background-color: #f8f9fa;
    color: #6c757d;
    border: none;
  }
  
  .card {
    border-radius: 8px;
    overflow: hidden;
  }
  
  .card-header {
    font-size: 1.1rem;
  }
  
  textarea {
    resize: none;
  }
  
  #message-history {
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .container {
    max-width: 700px;
  }
  
  </style>
  