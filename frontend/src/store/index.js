import {createStore} from "vuex";

export default createStore({
    state(){
    return {
        user: {
            roles: [],
            token: null,
            user_id:null,
        }
    }},
    
    getters: {
        getRoles(state){
            return state.user["roles"]
        },
    },
    mutations: {
        setUser(state, payload){
            state.user['roles'] = payload['roles'] || [];
            state.user['token'] = payload['token'];
            state.user['user_id'] = payload['user_id'];
            localStorage.setItem("user", JSON.stringify(state.user));
        }
    },
})