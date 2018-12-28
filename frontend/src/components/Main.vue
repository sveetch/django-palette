<template>
    <div class="app-root">
        <h2>{{ message }}</h2>
        <source-form></source-form>
        <palette-form v-if="openedParts.includes('palette')"></palette-form>
    </div>
</template>

<script>
import SourceForm from './SourceForm.vue';
import PaletteForm from './PaletteForm.vue';

export default {
    name: 'main-container',
    components: {
        SourceForm,
        PaletteForm
    },
    data() {
        return {
            openedParts: ['source'],
            message: 'Fill your colors'
        };
    },
    created() {
        // Listening events to enable/disable app parts, this is pretty naive
        // TODO: It should not try to add already enabled part
        this.$root.$on('enable_component_part', (part) => {
            this.openedParts.push(part);
            console.log("Enabled part: %s", part);
        });
        this.$root.$on('disable_component_part', (part) => {
            this.openedParts = this.openedParts.filter(item => item !== part)
            console.log("Disabled part: %s", part);
        });
    }
};
</script>
