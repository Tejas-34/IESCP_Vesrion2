
<script setup>
  import store from '@/store'
  import { RouterLink } from "vue-router";
  import router from '@/router'
</script>


<template>
  <div class="container-fluid">
    <div class="card row col-md-6 pb-5 login-card" >
      <div class="card-body">
        <div class="text-center ">
          <h2>Login</h2>
        </div>
        
          <form @submit.prevent="login"> 
            <div class="row">
              <div class="col">
                <input type="text" class="form-control" placeholder="Username" v-model="username" required>
              </div>
            </div>

            <div class="row">
              <div class="col">
                <input type="password" class="form-control" placeholder="Password" v-model="password" required>
              </div>
            </div>  
          
            <div class="row">
              <div class="col">
                <input to="/register" type="submit" class="btn btn-primary" >
                  <div class="invalid-feedback" :style="{display: (log) ? 'block' : 'none' }">
                      Login Failed check username or password.
                  </div>
              </div>

            </div>
            <p>Don't have an account? <router-link to="/signin" align="center">signin</router-link></p>
          </form>
      </div>
    </div>
  </div>
</template>



<script>

  export default {
    data() {
      return {
        username: null,
        password: null,
        log:false
      }
    },

    methods: {
      login() {

        fetch(import.meta.env.VITE_BASEURL+'/signin', 
        {method:"POST",
          headers: {'Content-Type': "application/json"},
          body: JSON.stringify({username:this.username, password:this.password})
        }).then(x=>{
          if(x.status == 200){
            return x.json();
          }
          else{
            this.log = true;
            router.push('/login')
          }
          return {}
        }).then(x=>{
          store.commit('setUser', x);
          console.log(x)
          this.checkRole(x);
        })
      },

      checkRole(x) {
        if(store.getters.getRoles.includes('influencer')){
          router.push('/influencer');
          
        }
        else if(store.getters.getRoles.includes('sponsor')){
          console.log(x['approve'])
            if(x['approve'] === false ){
              router.push('/signin/pending')
            }
            else{
              router.push('/sponsor')}
            
        }
        else if(store.getters.getRoles.includes('admin')){
          router.push('/admin')
        }
      },
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

  .login-card{
    box-shadow: 0px 0px 20px rgba(0,0,0.1); 
    border-radius: 8px; 
    max-width: 500px;
    min-height: 350px;
  }

  .btn-primary {
    width: 100%;
  }

  .row {
    padding: 10px 0 10px 0;
  }
</style>

