<template>
    <div class="output-part">
        <h2>Outputs</h2>

        <div class="fragments" v-if="fragments.length">
            <div class="item" v-bind:class="item.key" v-for="item in fragments">
                <h3>{{ item.key }} - {{ item.name }}</h3>
                <pre>{{ item.content }}</pre>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "output-part",
    data() {
        return {
        };
    },
    computed: {
        fragments: function () {
            return this.$store.state.output.fragments;
        },
    },
    methods: {
    }
};
</script>
