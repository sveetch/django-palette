<template>
    <div class="output-part block auto-alt" id="part-output">
        <div class="row">
            <div class="columns small-12">
                <h2 class="text-center v-space-short bottom-only">4. Output</h2>

                <div class="fragments flex-grid marged" v-if="fragments.length">
                    <div class="item cell large-50" v-bind:class="item.key" v-bind:id="itemContainerId(item.key)" v-for="item in fragments">
                        <h3>{{ item.name }}</h3>
                        <div class="content">
                            <button class="button modest tiny" v-on:click="copyText($event, item)">Copy to clipboard</button>
                            <pre class="box tiny gray99">{{ item.content }}</pre>
                        </div>
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
            activated_item: null,
            activated_interval_id: null,
        };
    },
    computed: {
        fragments: function () {
            return this.$store.state.output.fragments;
        },
    },
    // Mind to clear active timer if any before component is destroyed
    beforeDestroy () {
       clearInterval(this.activated_interval_id);
    },
    methods: {
        //
        // Return some element id for an output item
        //
        itemContainerId: function (key) {
            return "output-container-" + key;
        },

        //
        // Copy output content to clipboard
        //
        copyText (evt, item) {
            // Create temporary hided textarea element to contain content
            let container = document.querySelector("#" + this.itemContainerId(item.key));
            var textarea = document.createElement('textarea');
            textarea.value = item.content;
            textarea.setAttribute('readonly', '');
            textarea.style.position = 'absolute';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);

            // Copy content
            textarea.select();
            try {
                document.execCommand('copy');
                container.classList.add("active");
                // Put a temporary "active" flag on output container
                this.activated_item = item;
                this.set_active_timer();
            } catch(err) {}

            // Remove temporary element
            textarea.remove();
        },
        // Set timer for "active" callback
        set_active_timer () {
            this.activated_interval_id = setInterval(() => {
                let container = document.querySelector("#" + this.itemContainerId(this.activated_item.key));
                container.classList.remove("active");
                clearInterval(this.activated_interval_id);
            }, 500)
        }
    }
};
</script>
