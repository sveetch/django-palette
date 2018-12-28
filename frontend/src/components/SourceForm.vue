<template>
    <form id="source-form">
        <ul class="global error" v-if="errors._global">
            <li v-for="item in errors._global">
                {{ item }}
            </li>
        </ul>

        <div class="holder textarea">
            <p>Paste some hexadecimal codes</p>
            <textarea v-model="source" placeholder="Give me some source" required></textarea>
            <p class="error" v-if="errors.source">
                <span v-for="item in errors.source">
                    {{ item }}
                </span>
            </p>
        </div>

        <div class="holder buttons">
            <button type="button" v-on:click="resetSourceForm">Reset</button>
            <button type="button" v-on:click="submitSourceForm">Submit</button>
        </div>
    </form>
</template>


<script>
import { error_logger } from '../loggers.js';

// Initial errors data to use to start or reset errors
const initial_errors = {
    _global: [],
    source: []
};

export default {
    name: 'source-part',
    data() {
        return {
            errors: initial_errors,
            source: '#000000'
        };
    },
    computed: {
        // Deprecated
        global_errors: function () {
            console.log("global_errors");
            if(this.errors.hasOwnProperty('_global')){
                return this.errors['_global'];
            }

            return null;
        },
        // Deprecated
        source_errors: function () {
            console.log("source_errors");
            if(this.errors.hasOwnProperty('source')){
                return this.errors['source'];
            }

            return null;
        },
    },
    methods: {
        /* Just reset form fields and errors */
        resetSourceForm: function () {
            console.log("Reseted source form");
            this.source = '';
            this.errors = initial_errors;
        },
        /* Submit source to form validation */
        submitSourceForm: function () {
            console.log("Submited source form");

            this.errors = initial_errors;

            // Post with axios instance
            this.axios.post('/source/', {
                source: this.source
            })
            .then(
                response => {
                    console.log("Post request succeed");
                    // Enable palette part
                    this.$root.$emit('enable_component_part', 'palette');
                }
            )
            .catch(
                error => {
                    console.log("Post request failed");
                    this.errors = error_logger(this.errors, error);
                    // Disable palette part
                    this.$root.$emit('disable_component_part', 'palette');
                }
            );
        }
    }
};
</script>
