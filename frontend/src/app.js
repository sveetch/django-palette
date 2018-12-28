import "@babel/polyfill";

import Vue from 'vue';
//import Vuex from 'vuex';
import VueCookie from 'vue-cookie';
import axios from 'axios';
import VueAxios from 'vue-axios'

import App from './components/Main.vue';


// Enable plugins
Vue.use(VueCookie);
Vue.use(VueAxios, axios)


// Push csrf token to axios header
// This is not reactive, if token is updated from further forms, it won't
// be bubbled up to axios header
// NOTE: Move this to created method ?
axios.interceptors.request.use((config) => {
    config.headers['X-CSRFToken'] = vm.$cookie.get('csrftoken');

    return config
});


// Start main app
var vm = new Vue({
    el: '#app',
    render: h => h(App)
});
