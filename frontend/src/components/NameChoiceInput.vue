<template>
    <div class="form-item">
        <p>{{ form_index }} - {{ source }}</p>
        <label v-for="(choice, key) in choices" :key="key" style="display: block">
            <input type="radio" :value="choice.name" v-model="selected" v-on:change="inputSelection($event, form_index)">{{ key }} {{ choice.name }}

            <span v-if="choice.code != 'custom'" style="display: inline-block; width: 20px; height: 20px; border: 1px solid black;" v-bind:style="{ backgroundColor: choice.code }"></span>

            <span v-else><input type="text" placeholder="Custom" v-on:input="inputCustomName($event, form_index)"></span>
        </label>
        <p class="error" v-if="field_name_errors">
            <span v-for="item in field_name_errors">
                {{ item }}
            </span>
        </p>
        <p class="error" v-if="field_color_errors">
            <span v-for="item in field_color_errors">
                {{ item }}
            </span>
        </p>
        <hr />
    </div>
</template>


<script>
export default {
    name: "name-choice-input",
    props: ['form_index', 'source', 'choices', 'initialselected', 'errors'],
    data() {
        return {
            selected: this.initialselected,
            custom: "",
        };
    },

    computed: {
        field_name_errors: function () {
            return (this.errors.hasOwnProperty("name")) ? this.errors.name : null;
        },
        field_color_errors: function () {
            return (this.errors.hasOwnProperty("color")) ? this.errors.color : null;
        },
    },

    methods: {
        //
        // Update form 'custom' state from typed value and pop it up to
        // PaletteForm store
        //
        inputCustomName: function (evt, form_index) {
            this.custom = evt.target.value;
            this.$store.commit({
                type: "palette/update_form_custom",
                key: form_index,
                value: this.custom,
            });
        },
        //
        // Update form 'selected' state from typed value and pop it up to
        // PaletteForm store
        //
        inputSelection: function (evt, form_index) {
            this.$store.commit({
                type: "palette/update_form_selected",
                key: form_index,
                value: evt.target.value,
            });
        },
    }
};
</script>
