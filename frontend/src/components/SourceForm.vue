<template>
    <div class="source-part block auto-alt" id="part-source">
        <div class="row">
            <div class="columns small-12">
                <h2 class="text-center v-space-short bottom-only">1. Fill your colors</h2>
                <form>
                    <ul class="global error" v-if="global_errors.length">
                        <li v-for="item in global_errors">
                            {{ item }}
                        </li>
                    </ul>

                    <div class="holder textarea">
                        <textarea v-model="source" placeholder="Give me some source" required></textarea>
                        <p class="error" v-if="source_errors.length">
                            <span v-for="item in source_errors">
                                {{ item }}
                            </span>
                        </p>
                    </div>

                    <div class="holder button-group right">
                        <button class="button important hollow alert" type="button" v-on:click="resetForm">Reset</button>
                        <button class="button important" type="button" v-on:click="submitForm">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "source-part",
    data() {
        return {
            // TODO: Should be empty after final development stage
            source: "#000000\n#ffffff\n#404040\n#fefefe\n#022e4b\n#0a507c\n#1689b9\n#edf8ff\n#38393d\n#b5b8c4\n#f3f5fb"
        };
    },
    computed: {
        global_errors: function () {
            return this.$store.state.source.errors["_global"];
        },
        source_errors: function () {
            return this.$store.state.source.errors["source"];
        },
    },
    methods: {
        //
        // Reset form fields and errors
        //
        resetForm: function () {
            this.source = "";
            this.$store.dispatch({
                type: "source/resetErrors"
            });
        },

        //
        // Submit source to form validation
        //
        submitForm: function () {
            this.$store.dispatch({
                type: "source/sendForm",
                source: this.source
            });
        }
    }
};
</script>
