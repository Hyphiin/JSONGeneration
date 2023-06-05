<template>
  <div class="column items-center justify-start">
    <h3>Wireframe Detector</h3>
    <q-uploader
      url="http://127.0.0.1:5000/predict"
      style="max-width: 300px; margin-bottom: 20px"
      @uploaded="handleUploaded"
    />
    <div>
      <img :src="base64ImageString" alt="Resulting Image" width="1000" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ExampleComponent',
  props: {},
  setup() {
    const response = ref<string>('');
    const base64ImageString = ref<string>(''); // This will hold the base64 string

    const handleUploaded = (event: any) => {
      console.log('hello?', event);
      // The response from the server is in event.files[0].xhr.response
      const serverResponse = event.files[0].xhr.response;

      // If your server response is JSON, parse it
      const data = JSON.parse(serverResponse);

      // Now data should be the object you sent from the server
      console.log('DATA: ', data); // Log the data
      response.value = data;

      base64ImageString.value = 'data:image/jpeg;base64,' + data.image;
    };
    return { response, base64ImageString, handleUploaded };
  },
});
</script>
