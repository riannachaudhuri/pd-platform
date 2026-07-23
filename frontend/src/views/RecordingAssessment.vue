<template>

  <Navbar />

  <div class="min-h-screen bg-slate-100 py-10 px-6">

    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-3xl mx-auto overflow-hidden">

      <!-- Header -->

      <div class="bg-blue-600 text-white p-8">

        <h1 class="text-3xl font-bold">
          Voice Assessment
        </h1>

        <p class="mt-2 text-blue-100">
          AI Assisted Parkinson's Disease Screening
        </p>

      </div>

      <div class="p-10">

  <div
    v-if="!assessmentStarted"
    class="text-center py-10"
  >

    <h2 class="text-3xl font-bold">
      Voice Recording Assessment
    </h2>

    <p class="mt-5 text-slate-600 leading-8 max-w-xl mx-auto">

      You will complete five guided voice recordings.

      Each recording lasts approximately
      6 seconds.

      Please remain in a quiet environment
      and speak clearly into your microphone.

    </p>

    <button
      @click="startAssessment"
      class="mt-10 bg-blue-600 hover:bg-blue-700 text-white px-10 py-4 rounded-2xl font-semibold transition"
    >

      Start Assessment

    </button>

  </div>

  <div v-else>

    <!-- Progress -->

    <div class="mb-8">

      <div class="flex justify-between mb-2 text-sm text-slate-600">

        <span>
          Recording {{ currentStep + 1 }} of {{ recordings.length }}
        </span>

        <span>
          {{ progress }}%
        </span>

      </div>

      <div class="w-full bg-slate-200 rounded-full h-3">

        <div
          class="bg-blue-600 h-3 rounded-full transition-all duration-500"
          :style="{ width: progress + '%' }"
        ></div>

      </div>

    </div>

    <!-- Current Recording -->

    <div
      v-if="!finished"
      class="text-center"
    >

      <h2 class="text-2xl font-bold">

        {{ recordings[currentStep].label }}

      </h2>

      <p class="text-5xl font-black text-blue-700 mt-3">

        {{ recordings[currentStep].sound }}

      </p>

      <p class="mt-5 text-slate-600 leading-7">

        {{ recordings[currentStep].instruction }}

      </p>

      <p class="text-sm text-slate-400 mt-4">

        Hold the sound continuously for approximately
        5–6 seconds.

      </p>

    </div>

    <!-- Countdown -->

    <div
      v-if="countdown > 0 && !isRecording"
      class="text-center mt-14"
    >

      <div class="text-8xl font-black text-blue-600">

        {{ countdown }}

      </div>

      <p class="mt-3 text-slate-500">

        Recording begins shortly...

      </p>

    </div>
    
       <!-- Recording -->

<div
  v-show="isRecording"
  class="mt-12"
>

  <div class="flex justify-center">

    <div
      class="w-6 h-6 bg-red-600 rounded-full animate-pulse"
    ></div>

  </div>

  <p class="text-center mt-4 font-semibold">

    Recording...

  </p>

  <canvas
  ref="waveCanvas"
  width="700"
  height="120"
  class="w-full mt-8 rounded-xl bg-slate-900"
></canvas>

  <div class="text-center mt-5">

    {{ recordingTime.toFixed(1) }} sec

  </div>

</div>

<!-- Saved -->

<div
  v-if="finished && !assessmentComplete"
  class="text-center mt-10"
>

  <div class="text-7xl text-green-500">

    ✓

  </div>

  <h2 class="mt-4 text-2xl font-bold">

    Recording Saved

  </h2>

  <p class="mt-3 text-slate-500">

    Preparing the next phonation...

  </p>

</div>

<!-- Uploading -->

<div
  v-if="assessmentComplete"
  class="text-center py-16"
>

  <div
    class="animate-spin rounded-full h-20 w-20 border-b-4 border-blue-600 mx-auto"
  ></div>

  <h2 class="mt-8 text-3xl font-bold">

    Analyzing Voice Assessment...

  </h2>

  <p class="mt-3 text-slate-500">

    Uploading recordings and generating AI prediction.

  </p>

</div>

</div> <!-- closes v-else -->

</div>

</div>

</div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue"

import { ref, computed , onMounted } from "vue"
import { useRouter } from "vue-router"
import { useRecorder } from "../composables/useRecorder"

const router = useRouter()
const waveCanvas = ref(null)

const {
  startRecording,
  isRecording,
  recordingTime
} = useRecorder()

const recordings = [

  {
    label: "Recording 1",
    sound: "VE",
    instruction: 'Say "VEEEEEEEE" continuously.',
    key: "ve"
  },

  {
    label: "Recording 2",
    sound: "VI",
    instruction: 'Say "VIIIIIIII" continuously.',
    key: "vi"
  },

  {
    label: "Recording 3",
    sound: "VO",
    instruction: 'Say "VOOOOOOOO" continuously.',
    key: "vo"
  },

  {
    label: "Recording 4",
    sound: "VU",
    instruction: 'Say "VUUUUUUUU" continuously.',
    key: "vu"
  },

  {
    label: "Recording 5",
    sound: "D2",
    instruction: 'Repeat "D2 D2 D2..." continuously.',
    key: "d2"
  }

]

const currentStep = ref(0)
const countdown = ref(3)
const finished = ref(false)
const assessmentComplete = ref(false)

const audioFiles = ref([])
const assessmentStarted = ref(false)

const progress = computed(() =>
  Math.round(
    ((currentStep.value + 1) / recordings.length) * 100
  )
)

async function startAssessment() {

 assessmentStarted.value = true

  currentStep.value = 0

  await beginCountdown()

}

async function beginCountdown() {

  finished.value = false

  countdown.value = 3

  while (countdown.value > 0) {

    await new Promise(resolve =>
      setTimeout(resolve, 1000)
    )

    countdown.value--

  }

  await recordCurrentPhonation()

}

async function recordCurrentPhonation() {

  finished.value = false

  const blob = await startRecording(
  6000,
  waveCanvas.value
)

  audioFiles.value.push({

    key: recordings[currentStep.value].key,

    blob

  })

  finished.value = true

  if (currentStep.value < recordings.length - 1) {

    setTimeout(() => {

      currentStep.value++

      beginCountdown()

    }, 1200)

  }

  else {

    assessmentComplete.value = true

    uploadAssessment()

  }

}

async function uploadAssessment() {

  try {

    const formData = new FormData()

    audioFiles.value.forEach(file => {

      formData.append(
        file.key,
        file.blob,
        `${file.key}.wav`
      )

    })

    const response = await fetch(

      "https://voxora-46kt.onrender.com/predicts",

      {

        method: "POST",

        body: formData

      }

    )

    const result = await response.json()

    if (!response.ok) {

      alert(result.detail || "Assessment failed.")

      return

    }

    router.push({

      path: "/results",

      query: {

        diagnosis: result.diagnosis,

        confidence: result.confidence

      }

    })

  }

  catch (err) {

    console.error(err)

    alert("Unable to connect to server.")

  }

}



</script>