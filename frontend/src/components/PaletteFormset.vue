<template>
    <form id="palette-form">
        <h2>Name them</h2>

        <ul class="global error" v-if="global_errors">
            <li v-for="item in global_errors">
                {{ item }}
            </li>
        </ul>

        <div class="formset">
            <name-choice-input v-for="(form_data, form_index) in formset"
                               :key="form_index"
                               v-bind:form_index="form_index"
                               v-bind:source="form_data.source"
                               v-bind:choices="form_data.choices"
                               v-bind:initialselected="form_data.selected"
                               v-bind:errors="form_data.errors"
            ></name-choice-input>

            <h3>Formset</h3>
            <pre>{{ formset }}</pre>
            <hr />

            <h3>Payload</h3>
            <pre>{{ payload }}</pre>
            <hr />
        </div>

        <div class="holder buttons">
            <button type="button" v-on:click="submitForm">Submit</button>
        </div>
    </form>
</template>


<script>
import NameChoiceInput from "./NameChoiceInput.vue";

const FORMSET_FIELD_PREFIX = "form";

export default {
    name: "palette-part",
    components: {
        NameChoiceInput,
    },
    data() {
        return {};
    },

    computed: {
        global_errors: function () {
            return this.$store.state.palette.errors["_global"];
        },
        // Temporary shortcuts to display and debug datas
        formset: function () {
            return this.$store.state.palette.formset;
        },
        payload: function () {
            return this.$store.state.palette.data;
        },
    },

    methods: {
        //
        // Build valid formset field name
        // 'key' is optionnal but should be an integer for field index (zero
        // based) in formset
        //
        fieldname: function (name, key) {
            if(key){
                return FORMSET_FIELD_PREFIX + "-" + key + "-" + name;
            } else {
                return FORMSET_FIELD_PREFIX + "-" + name;
            }
        },

        //
        // Build request payload and send it to API
        //
        submitForm: function () {
            // Boot color name selection from form fields, it will be
            // structured as formset fields exactly how Django formset attempt
            // it
            let selection = {};

            // Add formset parameters
            selection[this.fieldname("TOTAL_FORMS")] = this.$store.state.palette.formset.length;
            selection[this.fieldname("INITIAL_FORMS")] = this.$store.state.palette.formset.length;
            selection[this.fieldname("MAX_NUM_FORMS")] = "";

            // Loop on every form to get selection
            for (let i in this.$store.state.palette.formset) {
                let item = this.$store.state.palette.formset[i];

                selection[this.fieldname("color", i)] = item.source;

                if(item.selected == "custom"){
                    selection[this.fieldname("name", i)] = item.custom;
                } else {
                    selection[this.fieldname("name", i)] = item.selected;
                }
            }

            // Send payload to API form
            this.$store.dispatch({
                type: "palette/sendForm",
                data: selection
            });
        }
    }
};
</script>
