import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LoginView from '@/views/LoginView.vue'
import index from '@/views/index.vue'
import AdminDashboard from '@/views/Admin/adminDashboard.vue'
import Registration from '@/views/Signin/Registration.vue'
import registractionSucces from '@/views/Signin/registractionSucces.vue'
import InfluDashboard from '@/views/Influencer/influDashboard.vue'
import SponDashboard from '@/views/Sponsor/sponDashboard.vue'
import SigninView from '@/views/Signin/SigninView.vue'
import Home from '@/views/Influencer/Home.vue'
import InfUpdateProfile from '@/views/Influencer/InfUpdateProfile.vue'
import InfAdRequest from '@/views/Influencer/infAdRequest.vue'
import InfSCamp from '@/views/Influencer/InfSCamp.vue'
import SpoHome from '@/views/Sponsor/SpoHome.vue'
import SpoUpdatePro from '@/views/Sponsor/SpoUpdatePro.vue'
import SpoMyCamp from '@/views/Sponsor/Campaign/SpoMyCamp.vue'
import SpoCreCamp from '@/views/Sponsor/SpoCreCamp.vue'
import SpoSearchInf from '@/views/Sponsor/AdRequest/SpoSearchInf.vue'
import SpoCampReqRec from '@/views/Sponsor/SpoRecReq.vue'
import VerificationView from '@/views/Signin/VerificationView.vue'
import CampUpdate from '@/views/Sponsor/Campaign/CampUpdate.vue'
import SpoRequest from '@/views/Sponsor/AdRequest/SpoRequest.vue'
import Negotiation from '@/views/Negotiation.vue'
import SpoCampReq from '@/views/Sponsor/SpoCampReq.vue'
import InfAllRequest from '@/views/Influencer/InfAllRequest.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: index
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    {
      path: '/signin',
      name: 'signin',
      component: SigninView,

      children: [
        {
          path: '',
          name: 'Registration',
          component: Registration,
        },
        {
          path: 'suc',
          name: 'registraction-success',
          component: registractionSucces
        },
        {
          path: 'pending',
          name: 'verifying',
          component: VerificationView
        },
        
      ]
    },


    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      children: [
        {
          path: '',
          name: 'AdminHome',
          component: '',
        }
      ]
    },

    {
      path: '/influencer',
      name: 'inf-Nav',
      component: InfluDashboard,

      children: [{
        path: '',
        name: 'Home',
        component: Home,
      },

      {
        path: 'infupdate',
        name: 'Update Profile',
        component: InfUpdateProfile,
      },

      {
        path: 'AdRequest',
        name: 'AdRequest',
        component: InfAdRequest,
      },

      {
        path: 's_camp',
        name: 'Search Campaign',
        component: InfSCamp,
      },
      {
        path: '/AllRequest',
        name: 'AllRequest',
        component: InfAllRequest,
      },

      {
        path: '/negotiation/:id',
        name: 'InfNegotiation',
        component: Negotiation,
      },

      ]
    },


    {
      path: '/sponsor',
      name: 'sponsor_dashboard',
      component: SponDashboard,
      children: [
        {
          path: '',
          name: 'SpoHome',
          component: SpoHome,
        },
        {
          path: 'UpdatePro',
          name: 'SpoUpdatePro',
          component: SpoUpdatePro,
        },
        {
          path: 'CampReqTotal',
          name: 'SpoCamReqTotal',
          component: SpoCampReq,
        },
        {
          path: 'Camp',
          name: 'MyCampaign',
          component: SpoMyCamp,
        },
        {
          path: 'CreatCamp',
          name: 'createCampaign',
          component: SpoCreCamp,
        },
        {
          path: 'SearchInf',
          name: 'SearchInfluencer',
          component: SpoSearchInf,
        },
        {
          path: 'CampReq',
          name: 'CampaignRequest',
          component: SpoCampReqRec,
        },
        {
          path: 'CampUpdate/:id',
          name: 'UpdateCampaign',
          component: CampUpdate,
        },
        {
          path: 'Request/:id/:name',
          name: 'Request',
          component: SpoRequest,
        },
        {
          path: '/negotiation/:id',
          name: 'SpoNegotiation',
          component: Negotiation,
        },
        
      ]
    },
    

  ]
})



router.beforeEach((to, from) => {                        //check every time when route execute
  if (to.fullPath.match(/[/]admin*/)) {                   //ensure that only admin should acces their dashboard
    if (store.getters.getRoles.includes("admin")) {
      return true
    }
    else {
      router.push('/login');
    }
  }
})
export default router