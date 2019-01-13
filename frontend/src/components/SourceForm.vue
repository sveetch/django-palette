<template>
    <div class="source-part">
        <h2>Fill your colors</h2>
        <form id="source-form">
            <ul class="global error" v-if="global_errors">
                <li v-for="item in global_errors">
                    {{ item }}
                </li>
            </ul>

            <div class="holder textarea">
                <p>Paste some hexadecimal codes</p>
                <textarea v-model="source" placeholder="Give me some source" required></textarea>
                <p class="error" v-if="source_errors">
                    <span v-for="item in source_errors">
                        {{ item }}
                    </span>
                </p>
            </div>

            <div class="holder buttons">
                <button type="button" v-on:click="resetForm">Reset</button>
                <button type="button" v-on:click="submitForm">Submit</button>
            </div>
        </form>
    </div>
</template>


<script>
export default {
    name: "source-part",
    data() {
        return {
            // TODO: Should be empty after final development stage
            source: "#000000\n#ffffff"
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
