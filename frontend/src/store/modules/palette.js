import qs from 'qs';

import { build_error_initials } from '../../utils/forms.js'


// Available SourceForm fields
const ALLOWED_FIELDNAMES = [];


const state = {
    // Errors
    // NOTE: This cant be static since it depends from received proposals,
    // move it to a getter ?
    errors: build_error_initials(ALLOWED_FIELDNAMES),
    // Color name proposals return by form from given source extraction
    proposals: {}
};


const getters = {};


const actions = {
};


const mutations = {
    update_proposals (state, payload) {
        state.proposals = payload.data;
    },
};


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
