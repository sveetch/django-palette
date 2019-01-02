import Vue from 'vue';
import VueCookie from 'vue-cookie';
import axios from 'axios';
import VueAxios from 'vue-axios'

import store from './store/index.js';

import MainContainer from './components/Main.vue';


// Enable plugins
Vue.use(VueCookie);
Vue.use(VueAxios, axios)

// NOTE: Move this to created method from main component ?
axios.interceptors.request.use((config) => {
    // Push csrf token to axios header
    // This is not reactive, if token is updated from further forms, it won't
    // be bubbled up to axios header
    config.headers['X-CSRFToken'] = vm.$cookie.get('csrftoken');
    // Send every POST request as urlencoded values since it does not seems to
    // have any proper way for Django to receive form data from
    // 'application/json' (it seems to works but fail django test client)
    config.headers['content-type'] = 'application/x-www-form-urlencoded';

    return config
});


// Start main app
var vm = new Vue({
    el: '#app',
    store,
    render: h => h(MainContainer)
});
