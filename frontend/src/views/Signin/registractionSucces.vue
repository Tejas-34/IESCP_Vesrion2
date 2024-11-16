
<template>
    
        
  <div class="container mt-5">
    <div class="success-container text-center">
      <h3>Registration Successful!</h3>
      <p class="lead">
        Congratulations, your registration has been completed successfully. You can now proceed to your dashboard or log in to access your account.
      </p>

      <div class="d-flex justify-content-center">
        <a href="/login" class="btn btn-success mx-2">Go to Login</a>
      </div>
    </div>
    </div>
</template>

<style scoped>
    .success-container {
      max-width: 600px;
      margin: 100px auto;
      padding: 40px;
      background-color: #ffffff;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .success-container h3 {
      font-size: 1.5rem;
      margin-bottom: 20px;
    }

    .success-container .btn {
      margin-top: 20px;
    }
</style>