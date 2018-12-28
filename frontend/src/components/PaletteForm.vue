<template>
    <form id="palette-form">
        <ul class="global error" v-if="errors._global">
            <li v-for="item in errors._global">
                {{ item }}
            </li>
        </ul>

        <div class="color-grid">
            <div class="cell" v-for="item in colors">
                <p>A color</p>
            </div>
        </div>

        <div class="holder buttons">
            <button type="button" v-on:click="submitPaletteForm">Submit</button>
        </div>
    </form>
</template>


<script>
import { error_logger } from '../loggers.js';

// Initial errors data to use to start or reset errors
const initial_errors = {
    _global: [],
    colors: {}
};

export default {
    name: 'palette-part',
    data() {
        return {
            errors: initial_errors,
            colors: []
        };
    },
    computed: {},
    methods: {
        /* Submit source to form validation */
        submitPaletteForm: function () {
            console.log("Submited source form");

            this.errors = initial_errors;

            // Post with axios instance
            this.axios.post('/palette/', {
                //source: this.source
            })
            .then(
                response => {
                    console.log("Post request succeed");
                    //console.log(response);
                }
            )
            .catch(
                error => {
                    console.log("Post request failed");
                    this.errors = error_logger(this.errors, error);
                }
            );
        }
    }
};
</script>
