import { build_error_initials } from "../../utils/forms.js"


// Available SourceForm fields
const ALLOWED_FIELDNAMES = ["source"];


const state = {
    // Form errors
    errors: build_error_initials(ALLOWED_FIELDNAMES),
    // Extracted colors from posted source
    colors: {},
    // Flag to indicate if form is working on submited data or not
    working: false,
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
        commit({
            type: "disable_submit"
        });
        dispatch({
            type: "resetErrors"
        });

        // Enable again current part to ensure following parts are destroyed
        dispatch({
            type: "enablePart",
            name: "source",
            noscroll: true,
        }, { root: true });

        // Post with axios instance
        this._vm.axios.post("/source/", {
            source: payload.source
        })
        .then(
            response => {
                console.log("Post request succeed from store");
                commit({
                    type: "enable_submit"
                });

                // Transmit returned name proposals from given source
                // TODO: Reset Palette name choice inputs
                dispatch({
                    type: "palette/receiveProposals",
                    data: response.data.data,
                }, { root: true });
                dispatch({
                    type: "enablePart",
                    name: "palette",
                }, { root: true });
            }
        )
        .catch(
            error => {
                commit({
                    type: "enable_submit"
                });
                // Back to source form part
                dispatch({
                    type: "enablePart",
                    name: "source",
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
    },

    // Manage form availability
    enable_submit (state, payload) {
        state.working = false;
    },
    disable_submit (state, payload) {
        state.working = true;
    },

};


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
