<template>
    <div class="dump-part block auto-alt" id="part-dump">
        <div class="row">
            <div class="columns small-12">
                <h2 class="text-center v-space-short bottom-only">3. Select formats</h2>

                <form>
                    <ul class="global error" v-if="global_errors.length || palette_errors.length">
                        <li v-for="item in global_errors">
                            {{ item }}
                        </li>
                        <li v-for="item in palette_errors">
                            {{ item }}
                        </li>
                    </ul>

                    <div class="holder checkbox-choices">
                        <div class="fields">
                            <label v-for="(choice, key) in available_formats" :key="key">
                                <input type="checkbox" :value="choice[0]" v-on:input="changeChoice($event, key)">
                                <span class="name">{{ choice[1] }}</span>
                            </label>
                        </div>
                        <p class="error" v-if="formats_errors.length">
                            <span v-for="item in formats_errors">
                                {{ item }}
                            </span>
                        </p>
                    </div>

                    <div class="holder button-group center">
                        <button class="button important full" type="button" v-on:click="submitForm">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "dump-part",
    data() {
        return {};
    },
    destroyed: function () {
        this.$store.dispatch({
            type: "dump/resetErrors"
        });
        // TODO: Reset selections
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
