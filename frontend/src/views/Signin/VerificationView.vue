<template>
<div class="container">
    <div class="verification-container">
      <h3>Profile Verification</h3>
      <div class="alert alert-info" role="alert">
        <strong>We are verifying your profile!</strong> Your registration details are under review by the admin. Please check back after some time.
      </div>

      <div class="alert alert-warning" role="alert">
        <strong>Note:</strong> You will be notified once your account has been approved or rejected.
      </div>

      <div class="d-flex justify-content-center">
        <router-link to="/login" class="btn btn-primary" align="center">Check Again Later</router-link>
      </div>
    </div>

</div>
</template>



<style scoped>
.verification-container {
      max-width: 600px;
      margin: 100px auto;
      padding: 40px;
      background-color: #ffffff;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .verification-container h3 {
      font-size: 1.5rem;
      margin-bottom: 20px;
    }

    .verification-container .alert {
      font-size: 1.1rem;
    }

    .verification-container .btn {
      margin-top: 20px;
    }
</style>

<script>

  export default {
    data() {
      return {
        username: null,
        password: null,
        log:false
      }
    },

  
}

</script>