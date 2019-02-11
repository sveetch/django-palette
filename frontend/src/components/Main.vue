<template>
    <div class="app-root">
        <SourceForm v-if="$store.getters.getOpenedParts.includes('source')"></SourceForm>
        <PaletteForm v-if="$store.getters.getOpenedParts.includes('palette')"></PaletteForm>
        <DumpForm v-if="$store.getters.getOpenedParts.includes('dump')"></DumpForm>
        <Output v-if="$store.getters.getOpenedParts.includes('output')"></Output>
    </div>
</template>


<script>
import SourceForm from "./SourceForm.vue";
import PaletteForm from "./PaletteFormset.vue";
import DumpForm from "./DumpForm.vue";
import Output from "./Output.vue";

export default {
    name: "main-container",
    components: {
        SourceForm,
        PaletteForm,
        DumpForm,
        Output
    },
    created() {
        // Allways starts with source form
        this.$store.commit({
            type: "enable_component_parts",
            parts: ["source"]
        });
    }
};
</script>
