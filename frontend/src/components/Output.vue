<template>
    <div class="output-part block auto-alt">
        <div class="row">
            <div class="columns small-12">
                <h2 class="text-center v-space-short bottom-only">4. Output</h2>

                <div class="fragments flex-grid marged" v-if="fragments.length">
                    <div class="item cell large-50" v-bind:class="item.key" v-for="item in fragments">
                        <h3>{{ item.name }}</h3>
                        <pre class="box tiny gray99">{{ item.content }}</pre>
                    </div>
                </div>
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
