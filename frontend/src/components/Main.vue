<template>
    <div class="app-root">
        <SourceForm v-if="$store.getters.getOpenedParts.includes('source')"></SourceForm>
        <PaletteForm v-if="$store.getters.getOpenedParts.includes('palette')"></PaletteForm>
        <FormatsForm v-if="$store.getters.getOpenedParts.includes('formats')"></FormatsForm>
        <Output v-if="$store.getters.getOpenedParts.includes('output')"></Output>
    </div>
</template>


<script>
import SourceForm from "./SourceForm.vue";
import PaletteForm from "./PaletteFormset.vue";
import FormatsForm from "./FormatsForm.vue";
import Output from "./Output.vue";

export default {
    name: "main-container",
    components: {
        SourceForm,
        PaletteForm,
        FormatsForm,
        Output
    },
    created() {
        // Allways starts on source form
        this.$store.dispatch({
            type: "enablePart",
            name: "source",
            noscroll: true,
        });
    }
};
</script>
