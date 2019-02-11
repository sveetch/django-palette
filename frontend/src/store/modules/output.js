const state = {
    // Extracted colors from posted source
    fragments: []
};


const getters = {};


const actions = {
    //
    // Receive datas from previous form
    //
    receive ({ state, commit, dispatch }, payload){
        commit({
            type: "update_fragments",
            fragments: payload.fragments,
        });
    },

};


const mutations = {
    // Manage sourceform errors
    update_fragments (state, payload) {
        state.fragments = payload.fragments;
    },
};


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
