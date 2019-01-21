import Vue from "vue";
import { build_error_initials } from "../../utils/forms.js"


// Available fields. Since formset is dynamic and depends from SourceForm
// return, there is no initial field
const ALLOWED_FIELDNAMES = [];


const state = {
    // Initial error structure
    errors: build_error_initials(ALLOWED_FIELDNAMES),
    // Color name proposals extracted and returned by source form
    proposals: {},
    // Set of forms created from proposals
    formset: [],
    // Formset datas to send
    data: {}
};


const getters = {};


const actions = {
    //
    // Receive proposals return by SourceForm to build palette form datas
    //
    receiveProposals ({ state, commit, dispatch }, payload){
        commit({
            type: "boot_proposals",
            data: payload.data,
        });

        commit({
            type: "reset_formset",
        });

        // Add each proposal as a formset item
        for (let code_source in state.proposals) {
            let choices = state.proposals[code_source].slice();
            choices.push(["custom", "custom"]);

            commit({
                type: "create_formset_form",
                code_source: code_source,
                choices: choices,
            });
        }
    },

    //
    // Reset source form states
    //
    resetErrors ({ commit }, payload){
        commit({
            type: "reset_errors"
        });
    },

    //
    // Send PaletteFormset to API
    //
    sendForm ({ state, commit, dispatch }, payload){
        dispatch({
            type: "resetErrors"
        });

        commit({
            type: "update_sended_data",
            data: payload.data,
        });

        // Post with axios instance
        this._vm.axios.post("/palette/", payload.data)
        .then(
            response => {
                console.log("Post palette request succeed from store");
            }
        )
        .catch(
            error => {
                dispatch({
                    type: "error_logger",
                    fields: ALLOWED_FIELDNAMES,
                    errorObject: error,
                    module: "palette"
                }, { root: true });
            }
        );
    },
};


const mutations = {
    //
    // Init proposals data into store
    //
    boot_proposals (state, payload) {
        state.proposals = payload.data;
    },

    //
    // Reset formset store datas
    //
    reset_formset (state) {
        state.formset = [];
    },

    //
    // Fill a formset item data from given proposal choices
    // This should be allways used after 'reset_formset' mutation
    //
    create_formset_form (state, payload) {
        let choices = [];
        for (let k in payload.choices) {
            choices.push({
                code: payload.choices[k][1],
                name: payload.choices[k][0]
            });
        }

        state.formset.push({
            source: payload.code_source,
            choices: choices,
            selected: choices[0].name,
            errors: {},
            custom: ""
        });
    },

    //
    // Change name choice selection on form
    //
    update_form_selected (state, payload) {
        state.formset[payload.key].selected = payload.value;
    },
    //
    // Change custom name on form
    //
    update_form_custom (state, payload) {
        state.formset[payload.key].custom = payload.value;
    },

    //
    // Change custom name on form
    //
    update_sended_data (state, payload) {
        state.data = payload.data;
    },

    //
    // Reset every formset errors
    //
    reset_errors (state, payload) {
        state.errors = build_error_initials(ALLOWED_FIELDNAMES);

        for (let key in state.formset) {
            Vue.set(state.formset[key], "errors", {});
        }
    },

    //
    // Store returned formset errors
    //
    update_errors (state, payload) {
        // Global slot
        if(payload.fields.hasOwnProperty("global")){
            //state.errors["_global"] = payload.fields.global;
            Vue.set(state.errors, "_global", payload.fields.global);
        }

        // Iterate through given fields except reserved 'global' slot
        for (let key in payload.fields) {
            if(key != "_global" && key != "global"){
                let pack = payload.fields[key],
                    name_errors = pack.hasOwnProperty("name") ? pack["name"] : null,
                    color_errors = pack.hasOwnProperty("color") ? pack["color"] : null;

                Vue.set(state.formset[key].errors, "name", name_errors);
                Vue.set(state.formset[key].errors, "color", color_errors);
            }
        }
    },
};


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
