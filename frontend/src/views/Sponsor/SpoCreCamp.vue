<template>
    <div class="content">
        <h2>Create Campaign</h2>
        <form @submit.prevent="campCreate">

            <div class="form-group mb-2">
                <label for="campaignName">Campaign Name</label>
                <input type="text" class="form-control" name="Name" id="campaignName" placeholder="Enter campaign name"
                    v-model="camp['Name']" required>
            </div>

            <div class="form-group mb-2">
                <label for="description">Description</label>
                <textarea class="form-control" id="description" name="Description" rows="4"
                    placeholder="Enter campaign description" v-model="camp['Description']" required></textarea>
            </div>

            <div class="form-group mb-2">
                <label for="startDate">Start Date</label>
                <input type="date" class="form-control" name="Start_date" id="startDate" v-model="camp['Start_date']"
                    required>
            </div>

            <div class="form-group mb-2">
                <label for="endDate">End Date</label>
                <input type="date" class="form-control" name="End_date" id="endDate" v-model="camp['End_date']"
                    required>
            </div>

            <div class="form-group mb-2">
                <label for="budget">Budget</label>
                <input type="number" class="form-control" name="Budget" id="budget" placeholder="Enter budget"
                    v-model="camp['Budget']" required>
            </div>

            <div class="form-group mb-2">
                <label for="visibility">Visibility</label>
                <select class="form-control" name="visibility" id="visibility" v-model="camp['visibility']" required>
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                </select>
            </div>

            <div class="form-group mb-2">
                <label for="goals">Goals</label>
                <textarea class="form-control" name="goal" id="goals" rows="3" placeholder="Enter campaign goals"
                    v-model="camp['goal']" required></textarea>
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

            <button type="submit" class="btn btn-primary">Create Campaign</button>
        </form>

    </div>
</template>


<script>

import router from '@/router';

export default {
    data() {
        return {
            camp: {
                Name: null,
                Description: null,
                Start_date: null,
                End_date: null,
                Budget: null,
                visibility: null,
                goal: null,
                category: null
            },
        }
    },

    methods: {
        campCreate() {
            const local = JSON.parse(localStorage.getItem("user"));
              // Log payload for debugging
            fetch(import.meta.env.VITE_BASEURL + '/sponsor/create_campaign', {
                method: "POST",
                headers: {
                    'Content-Type': "application/json",
                    'Authorization': 'Bearer ' + local.token
                },
                body: JSON.stringify(this.camp)
            })
                .then(response => {
                    if (response.status === 201) {
                        alert('Campaign created successfully');
                        router.push('/sponsor/Camp');
                    } else {
                        return response.json().then(error => {
                            console.error("Error from server:", error);
                            alert("Error: " + (error.msg || "Please check your input."));
                        });
                    }
                })
                .catch(error => console.error("Error during creation:", error));
        }
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