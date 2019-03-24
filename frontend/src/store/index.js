import Vue from "vue";
import Vuex from "vuex";
import VueScrollTo from "vue-scrollto"

import { build_error_initials } from "../utils/forms.js"
import source from "./modules/source"
import palette from "./modules/palette"
import dump from "./modules/dump"
import output from "./modules/output"


Vue.use(Vuex);

export default new Vuex.Store({
    // Enable vuex strict mode on development
    strict: process.env.NODE_ENV !== 'production',

    // Enabled component stores
    modules: {
        source,
        palette,
        dump,
        output
    },

    // Where stored datas will live
    state: {
        // Full ordered parts path
        available_parts: ["source", "palette", "dump", "output"],
        // Current active application parts
        opened_parts: [],
    },

    // Shared computed properties
    getters: {
        // Return current active app parts
        getOpenedParts (state, getters) {
            return state.opened_parts;
        }
    },

    // Actions are in charge to perform tasks which provoke mutations
    actions: {
        //
        // Common HTTP error logger.
        //
        // TODO: Make 'console.log' conditionnal to development environment or
        //       at least remove every ones.
        //
        // From given axios error response, manage different error kind to
        // component store.
        //
        // @fields: list of available form field names, field errors that does
        //          not match any of available names will be ignored.
        // @errorObject: Error object as returned from axios
        // @module: Optional module namespace to call commit/dispatch. If not
        //          given means root store level.
        //
        error_logger({ commit }, { fields, errorObject, module }){
            var opts = {};
            if(module){
                module = module + "/";
            } else {
                module = "";
                opts = { root: true };
            }

            if (errorObject.response) {
                console.log("Status: http%s", errorObject.response.status);

                if(errorObject.response.status == 400) {
                    console.log("Error returned from form");
                    commit({
                        type: module + "update_errors",
                        names: fields,
                        fields: errorObject.response.data.data
                    }, opts);
                } else if (errorObject.response.status == 500) {
                    console.log("Error server");
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": ["Internal Server Error"],
                        }
                    }, opts);
                } else if (errorObject.response.status == 404) {
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": ["Not Found"],
                        }
                    });
                } else {
                    console.log("Undetermined error");
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": [`Error http${errorObject.response.status} : ${errorObject.response.statusText}`],
                        }
                    }, opts);
                }
            } else if (errorObject.request) {
                // The request was made but no response was received
                console.log("Request error");
                commit({
                    type: module + "update_errors",
                    fields: {
                        "global": ["Server does not respond to request"],
                    }
                }, opts);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log("Error", errorObject.message);
            }
        },

        //
        enablePart({ commit, dispatch }, { name, noscroll }){
            commit({
                type: "enable_part",
                name: name
            });

            if(!noscroll){
                dispatch({
                    type: "scrolltoPart",
                    name: name,
                });
            }
        },

        // Enable parts and scroll to the last part
        scrolltoPart (state, { name }) {
            let target = "part-" + name;
            // Element does not exist yet, so wait for next tick to
            // perform scroll
            Vue.nextTick(function () {
                VueScrollTo.scrollTo(document.getElementById(target));
            });
        },
    },

    // State mutations
    mutations: {
        // Enable components parts
        enable_part (state, { name }) {
            let index = state.available_parts.lastIndexOf(name);
            let parts = state.available_parts.slice(0, index+1);
            state.opened_parts = parts;
        },
    }
});
