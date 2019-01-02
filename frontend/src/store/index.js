import Vue from 'vue';
import Vuex from 'vuex';
import qs from 'qs';

import { build_error_initials } from '../utils/forms.js'
import source from './modules/source'
import palette from './modules/palette'


Vue.use(Vuex);


export default new Vuex.Store({
    modules: {
        source,
        palette
    },

    // Where stored datas will live
    state: {
        // Current active application parts, order does not matter
        // NOTE: Pretty complicated for nothing, we could instead simply use a
        // boolean state for each part since it won't be more than three and
        // have a more simple way to enable/disable parts from an action like
        // 'gotoPart("palette")' or 'backtoPart("source")'
        opened_parts: [],
    },

    // Alike share computed properties
    getters: {
        // Return current active app parts
        getOpenedParts (state, getters) {
            return state.opened_parts;
        }
    },

    // Actions are in charge to perform job which provoke mutation
    actions: {
        // Common error logger
        // @fields: list of available form field names, field errors that does
        //          not match any of available names will be ignored.
        // @errorObject: Error object as returned from axios
        // @module: Optional module namespace to call commit/dispatch. If not
        //          given means root store level.
        error_logger({ commit }, { fields, errorObject, module }){
            var opts = {};
            if(module){
                module = module + "/";
            } else {
                module = "";
                opts = { root: true };
            }

            if (errorObject.response) {
                console.log("http %s", errorObject.response.status);

                if(errorObject.response.status == 400) {
                    console.log("Error returned from form");
                    commit({
                        type: module + 'update_errors',
                        names: fields,
                        fields: errorObject.response.data.data
                    }, opts);
                } else if (errorObject.response.status == 500) {
                    console.log("Error server");
                    commit({
                        type: module + 'update_errors',
                        fields: {
                            "global": ["Internal Server Error"],
                        }
                    }, opts);
                } else if (errorObject.response.status == 404) {
                    commit({
                        type: module + 'update_errors',
                        fields: {
                            "global": ["Not Found"],
                        }
                    });
                } else {
                    console.log("Undetermined error");
                    commit({
                        type: module + 'update_errors',
                        fields: {
                            "global": [`Error http${errorObject.response.status} : ${errorObject.response.statusText}`],
                        }
                    }, opts);
                }
            } else if (errorObject.request) {
                // The request was made but no response was received
                console.log("Request error");
                commit({
                    type: module + 'update_errors',
                    fields: {
                        "global": ["Server does not respond to request"],
                    }
                }, opts);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', errorObject.message);
            }
        },
    },

    // The only way to update state datas
    mutations: {
        // Manage components parts
        enable_component_parts (state, payload) {
            for (let key in payload.parts) {
                let part = payload.parts[key];
                if(!state.opened_parts.includes(part)) {
                    state.opened_parts.push(part);
                }
            }
        },
        disable_component_parts (state, payload) {
            for (let key in payload.parts) {
                state.opened_parts = state.opened_parts.filter(item => item !== payload.parts[key]);
            }
        },
    }
});
