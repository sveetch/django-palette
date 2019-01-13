<template>
    <div class="app-root">
        <source-form v-if="$store.getters.getOpenedParts.includes('source')"></source-form>
        <palette-form v-if="$store.getters.getOpenedParts.includes('palette')"></palette-form>
    </div>
</template>


<script>
import SourceForm from "./SourceForm.vue";
import PaletteForm from "./PaletteFormset.vue";

export default {
    name: "main-container",
    components: {
        SourceForm,
        PaletteForm
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
