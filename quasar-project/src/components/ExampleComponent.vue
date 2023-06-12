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

interface PredictionItem {
  class: string;
  confidence: number;
  height: number;
  width: number;
  x: number;
  y: number;
}

interface Component {
  id: number;
  predictionItem: PredictionItem;
  type: 'component';
}

interface Container {
  id: number;
  predictionItem: PredictionItem;
  type: 'container';
  children: Array<Container | Component>;
}

export default defineComponent({
  name: 'ExampleComponent',
  props: {},
  setup() {
    const base64ImageString = ref<string>('');

    // Helper function to determine if a container is inside another
    const isInside = (
      item: Component | Container,
      potentialParent: Container
    ): boolean => {
      return (
        item.predictionItem.x >= potentialParent.predictionItem.x &&
        item.predictionItem.y >= potentialParent.predictionItem.y &&
        item.predictionItem.x + item.predictionItem.width <=
          potentialParent.predictionItem.x +
            potentialParent.predictionItem.width &&
        item.predictionItem.y + item.predictionItem.height <=
          potentialParent.predictionItem.y +
            potentialParent.predictionItem.height
      );
    };

    const processPredictions = (predictions: PredictionItem[]) => {
      let containerStructure: Container[] = [];
      let conmponentStructure: Component[] = [];
      let idCounter = 0;

      // split containers and components and sort them
      let containers = predictions
        .filter((p) => p.class === 'container')
        .sort((a, b) => a.y - b.y || a.x - b.x);
      let components = predictions
        .filter((p) => p.class !== 'container')
        .sort((a, b) => a.y - b.y || a.x - b.x);

      // transform containers
      containers.forEach((item, i) => {
        containerStructure.push({
          id: idCounter++,
          predictionItem: item,
          type: 'container',
          children: [],
        });
      });

      // transform components
      components.forEach((item, i) => {
        conmponentStructure.push({
          id: idCounter++,
          predictionItem: item,
          type: 'component',
        });
      });

      // nest children inside their parents
      for (let i = conmponentStructure.length - 1; i >= 0; i--) {
        let currentItem = conmponentStructure[i];
        let smallestParentIndex = -1;
        let smallestParentSize = Infinity;
        for (let j = i - 1; j >= 0; j--) {
          let potentialParent = containerStructure[j];
          if (potentialParent !== undefined) {
            if (
              potentialParent.type === 'container' &&
              isInside(currentItem, potentialParent)
            ) {
              let potentialParentSize =
                potentialParent.predictionItem.width *
                potentialParent.predictionItem.height;
              if (potentialParentSize < smallestParentSize) {
                smallestParentIndex = j;
                smallestParentSize = potentialParentSize;
              }
            }
          }
        }

        if (smallestParentIndex !== -1) {
          (containerStructure[smallestParentIndex] as Container).children.push(
            currentItem
          );
          containerStructure.splice(i, 1);
        }
      }

      return containerStructure;
    };

    const handleUploaded = (event: any) => {
      console.log('hello?', event);
      const serverResponse = event.files[0].xhr.response;

      const data = JSON.parse(serverResponse);

      console.log('DATA: ', data);
      base64ImageString.value = 'data:image/jpeg;base64,' + data.image;

      const predictions: PredictionItem[] = data.predictions;

      const containerStructure = processPredictions(predictions);

      console.log(containerStructure);
    };

    return { base64ImageString, handleUploaded };
  },
});
</script>
