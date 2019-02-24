<template>
    <div class="form-item">
        <div class="tile" v-bind:style="{ backgroundColor: source }">
            <span class="code">{{ source }}</span>
        </div>

        <label v-for="(choice, key) in choices" :key="key" :class="labelClass(choice)">
            <input type="radio" :value="choice.name" v-model="selected" v-on:change="inputSelection($event, form_index)">

            <span class="name">{{ choice.name }}</span>

            <span v-if="choice.code != 'custom'" class="sample" v-bind:style="{ backgroundColor: choice.code }"></span>

            <span v-else class="custom-input">
                <input type="text" placeholder="Custom"
                       v-on:focus="inputSelection($event, form_index, 'custom')"
                       v-on:input="inputCustomName($event, form_index)">
            </span>
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
        //
        //
        labelClass: function (choice) {
            return (choice.code != "custom") ? "selection" : "custom";
        },

        //
        // Update form 'custom' state from typed value and pop it up to
        // PaletteForm store
        //
        enableSelection: function (evt, value) {
            this.selected = value;
        },

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
        inputSelection: function (evt, form_index, value) {
            if(value){
                this.selected = value;
            }

            this.$store.commit({
                type: "palette/update_form_selected",
                key: form_index,
                value: (value) ? value : evt.target.value,
            });
        },
    }
};
</script>
