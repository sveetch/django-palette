<template>
    <form id="palette-form">
        <h2>Name them</h2>

        <div class="formset">
            <div class="form" v-for="(proposals, code_source, form_index) in formset">
                <div :key='form_index'>
                    <p>{{ form_index }} - {{ code_source }}</p>
                    <label v-for="(value, key) in proposals" :key='key'>
                        <input type="radio" v-bind:value="value[1]"> {{ value[0] }}
                        <span style="display: inline-block; width: 20px; height: 20px; border: 1px solid black;" v-bind:style="{ backgroundColor: value[1] }"></span>
                    </label>
                </div>
                <div class='custom'>
                    <label>
                        <input type="radio" value="custom">
                    </label>
                    <input type="text" placeholder="Custom">
                </div>
                <hr />
            </div>
        </div>

        <div class="holder buttons">
            <button type="button" v-on:click="submitForm">Submit</button>
        </div>
    </form>
</template>


<script>
export default {
    name: 'palette-part',
    data() {
        return {
            colors: []
        };
    },

    computed: {
        global_errors: function () {
            return this.$store.state.palette.errors['_global'];
        },
        formset: function () {
            return this.$store.state.palette.proposals;
        },
    },

    methods: {
    }
};
</script>
