<template>
  <div class="column items-center justify-start">
    <h3>Wireframe Detector</h3>
    <q-uploader
      url="http://127.0.0.1:5000/predict"
      style="max-width: 300px; margin-bottom: 20px"
      @uploaded="handleUploaded"
    />
    <div>
      <img
        :src="base64ImageString"
        alt="Resulting Image"
        width="1000"
        height="800"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ExampleComponent',
  props: {},
  setup() {
    const base64ImageString = ref<string>('');

    const handleUploaded = (event: any) => {
      console.log('hello?', event);
      const serverResponse = event.files[0].xhr.response;

      const data = JSON.parse(serverResponse);

      console.log('DATA: ', data);

      base64ImageString.value = 'data:image/jpeg;base64,' + data.image;
    };
    return { base64ImageString, handleUploaded };
  },
});
</script>
