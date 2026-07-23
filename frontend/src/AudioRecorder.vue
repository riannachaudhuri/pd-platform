<template>
  <div>
    <h2>Parkinson's Voice Test</h2>

    <button @click="startRecording" :disabled="recording">
      Start Recording
    </button>

    <button @click="stopRecording" :disabled="!recording">
      Stop Recording
    </button>

    <p v-if="recording">
      Recording...
    </p>

    <audio 
      v-if="audioURL"
      :src="audioURL"
      controls
    />

    <button 
      v-if="audioBlob"
      @click="sendAudio"
    >
      Analyze Voice
    </button>
  </div>
</template>


<script setup>

import { ref } from "vue"


const mediaRecorder = ref(null)
const audioChunks = ref([])

const recording = ref(false)

const audioBlob = ref(null)
const audioURL = ref(null)



async function startRecording(){

    const stream = await navigator.mediaDevices.getUserMedia({
        audio:true
    })


    mediaRecorder.value = new MediaRecorder(stream)

    audioChunks.value = []


    mediaRecorder.value.ondataavailable = event => {

        if(event.data.size > 0){
            audioChunks.value.push(event.data)
        }

    }


    mediaRecorder.value.onstop = () => {

        audioBlob.value = new Blob(
            audioChunks.value,
            {
                type:"audio/wav"
            }
        )


        audioURL.value = URL.createObjectURL(
            audioBlob.value
        )

    }


    mediaRecorder.value.start()

    recording.value = true

}



function stopRecording(){

    mediaRecorder.value.stop()

    recording.value = false

}



async function sendAudio(){

    const formData = new FormData()


    formData.append(
        "file",
        audioBlob.value,
        "recording.wav"
    )


    const response = await fetch(
        "https://voxora-46kt.onrender.com/predict",
        {
            method:"POST",
            body:formData
        }
    )


    const result = await response.json()

    console.log(result)

}

</script>