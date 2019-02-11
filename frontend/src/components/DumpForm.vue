<template>
    <div class="dump-part">
        <h2>Dump them</h2>
        <form id="dump-form">
            <ul class="global error" v-if="global_errors.length || palette_errors.length">
                <li v-for="item in global_errors">
                    {{ item }}
                </li>
                <li v-for="item in palette_errors">
                    {{ item }}
                </li>
            </ul>

            <div class="holder checkbox-choices">
                <p>Select some dump formats</p>
                <div class="fields">
                    <label v-for="(choice, key) in available_formats" :key="key" style="display: block">
                        <input type="checkbox" :value="choice[0]" v-on:input="changeChoice($event, key)">{{ choice[1] }}
                    </label>
                </div>
                <p class="error" v-if="formats_errors.length">
                    <span v-for="item in formats_errors">
                        {{ item }}
                    </span>
                </p>
            </div>

            <div class="holder buttons">
                <button type="button" v-on:click="submitForm">Submit</button>
            </div>
        </form>
    </div>
</template>


<script>
export default {
    name: "dump-part",
    data() {
        return {
            selected_formats: [],
        };
    },
    computed: {
        global_errors: function () {
            return this.$store.state.dump.errors["_global"];
        },
        palette_errors: function () {
            return this.$store.state.dump.errors["palette"];
        },
        formats_errors: function () {
            return this.$store.state.dump.errors["formats"];
        },
        available_formats: function () {
            return this.$store.state.dump.available_formats;
        },
    },
    methods: {
        //
        // Update form 'custom' state from typed value and pop it up to
        // PaletteForm store
        //
        changeChoice: function (evt, input_index) {
            this.$store.commit({
                type: "dump/update_enabled_formats",
                key: evt.target.value,
                checked: evt.target.checked,
            });
        },

        //
        // Submit data to form validation
        //
        submitForm: function () {
            this.$store.dispatch({
                type: "dump/sendForm",
            });
        }
    }
};
</script>
