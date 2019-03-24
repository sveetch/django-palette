import { build_error_initials } from "../../utils/forms.js"


// Available SourceForm fields
const ALLOWED_FIELDNAMES = ["palette", "formats"];


const state = {
    // Form errors
    errors: build_error_initials(ALLOWED_FIELDNAMES),
    // Palette data
    palette: {},
    // Available formats
    available_formats: [],
    // Enabled formats from checkboxes
    enabled_formats: []
};


const getters = {};


const actions = {
    //
    // Receive datas from previous form
    //
    receive ({ state, commit, dispatch }, payload){
        commit({
            type: "boot_states",
            palette: payload.data.palette,
            available_formats: payload.data.formats,
        });
    },

    // Reset formats form states
    resetErrors ({ commit }, payload){
        commit({
            type: "reset_errors"
        });
    },

    // Perform formats POST request to backend
    sendForm ({ commit, dispatch }, payload){
        dispatch({
            type: "resetErrors"
        });

        // Post with axios instance
        this._vm.axios.post("/dump/", {
            palette: state.palette,
            formats: state.enabled_formats,
        })
        .then(
            response => {
                console.log("Post request succeed from formats store");
                dispatch({
                    type: "output/receive",
                    fragments: response.data.data,
                }, { root: true });

                // Enable formats part
                dispatch({
                    type: "enablePart",
                    name: "output",
                }, { root: true });
            }
        )
        .catch(
            error => {
                dispatch({
                    type: "error_logger",
                    fields: ALLOWED_FIELDNAMES,
                    errorObject: error,
                    module: "formats"
                }, { root: true });
            }
        );
    }
};


const mutations = {
    //
    // Init data into store
    //
    boot_states (state, payload) {
        state.palette = payload.palette;
        state.available_formats = payload.available_formats;
        state.enabled_formats = [];
    },

    //
    // Manage enabled formats
    //
    update_enabled_formats (state, payload) {
        // Add unique value
        if(payload.checked && !state.enabled_formats.includes(payload.key)){
            state.enabled_formats.push(payload.key);
        // Remove unique value
        } else {
            state.enabled_formats.splice(
                state.enabled_formats.indexOf(payload.key),
                1
            );
        }
    },

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
