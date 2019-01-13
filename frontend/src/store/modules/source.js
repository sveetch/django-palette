import qs from "qs";

import { build_error_initials } from "../../utils/forms.js"


// Available SourceForm fields
const ALLOWED_FIELDNAMES = ["source"];


const state = {
    // Form errors
    errors: build_error_initials(ALLOWED_FIELDNAMES),
    // Extracted colors from posted source
    colors: {}
};


const getters = {};


const actions = {
    // Reset source form states
    resetErrors ({ commit }, payload){
        commit({
            type: "reset_errors"
        });
    },

    // Perform source POST request to backend
    sendForm ({ commit, dispatch }, payload){
        dispatch({
            type: "resetErrors"
        });

        // Post with axios instance
        this._vm.axios.post("/source/", qs.stringify({
            source: payload.source
        }))
        .then(
            response => {
                console.log("Post request succeed from store");

                // Transmit returned name proposals from given source
                dispatch({
                    type: "palette/receiveProposals",
                    data: response.data.data,
                }, { root: true });

                // Enable palette part
                commit({
                    type: "enable_component_parts",
                    parts: ["palette"],
                }, { root: true });
            }
        )
        .catch(
            error => {
                console.log("Post request failed from store");
                // Back to source form part
                commit({
                    type: "disable_component_parts",
                    parts: ["palette"],
                }, { root: true });

                dispatch({
                    type: "error_logger",
                    fields: ALLOWED_FIELDNAMES,
                    errorObject: error,
                    module: "source"
                }, { root: true });
            }
        );
    }
};


const mutations = {
    // Manage sourceform errors
    reset_errors (state, payload) {
        state.errors = build_error_initials(ALLOWED_FIELDNAMES);
    },

    update_errors (state, payload) {
        // Global slot
        if(payload.fields.hasOwnProperty("global")){
            state.errors["_global"] = payload.fields.global;
        }
        // Iterate through given fields except reserved global slot
        for (let key in payload.fields) {
            if(key != "_global" && key != "global"){
                let value = payload.fields[key];
                // If allowed from form fieldname definition
                if(!payload.names || payload.names.includes(key)){
                    state.errors[key] = value;
                }
            }
        }
    }
};


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
